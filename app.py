import os
import json
import subprocess
import traceback

import numpy as np
from flask import Flask, render_template, request, jsonify

try:
    import joblib
except ImportError:
    import pickle as joblib

app = Flask(__name__)
BASE = os.path.dirname(os.path.abspath(__file__))

BEHAVIOR_LABELS = [
    'Highly Productive', 'Balanced', 'Social Heavy',
    'Gaming Addicted', 'Doom Scroller', 'Night Owl', 'Distracted'
]
TREND_LABELS = ['Improving', 'Stable', 'Declining', 'Critical']


def _load(filename):
    path = os.path.join(BASE, filename)
    try:
        obj = joblib.load(path)
        # unwrap dict-wrapped models: {'model': clf, ...}
        if isinstance(obj, dict):
            for key in ('model', 'classifier', 'estimator', 'clf', 'pipe', 'pipeline'):
                if key in obj:
                    return obj[key]
            # fallback: return first value that has predict
            for v in obj.values():
                if hasattr(v, 'predict'):
                    return v
        return obj
    except Exception as e:
        app.logger.error(f"Failed to load {filename}: {e}")
        return None


addiction_model = _load('addiction_model.pkl')
app_classifier  = _load('app_classifier.pkl')
trend_model     = _load('trend_model.pkl')


def _safe_predict(model, X):
    if model is None or not hasattr(model, 'predict'):
        return None
    try:
        return model.predict(X)[0]
    except Exception:
        try:
            return model.predict(X[:, :model.n_features_in_])[0]
        except Exception:
            return None


def _safe_proba(model, X, n_classes=7):
    if model is None or not hasattr(model, 'predict_proba'):
        return [1.0 / n_classes] * n_classes
    try:
        p = model.predict_proba(X)[0]
        return [float(v) for v in p]
    except Exception:
        try:
            n = getattr(model, 'n_features_in_', X.shape[1])
            p = model.predict_proba(X[:, :n])[0]
            return [float(v) for v in p]
        except Exception:
            return [1.0 / n_classes] * n_classes


def _run_calc(args):
    exe = os.path.join(BASE, 'calc.exe')
    if not os.path.isfile(exe):
        return {}
    try:
        res = subprocess.run(
            [exe] + [str(round(float(a), 4)) for a in args],
            capture_output=True, text=True, timeout=10
        )
        raw = (res.stdout or '').strip()
        if raw and raw.startswith('{'):
            return json.loads(raw)
    except Exception:
        pass
    return {}


def _build_features_16(vals):
    return np.array([vals], dtype=np.float64)


def _build_features_8(vals):
    screen, gaming, social, ai_tools, study, unlocks, notifs, switches, \
        focus, productivity, stress, sleep_, reels, youtube, chat, night = vals
    return np.array([[screen, social, gaming, reels, youtube, night, focus, productivity]], dtype=np.float64)


def _compute_fallbacks(screen, gaming, social, ai_tools, study, unlocks, notifs,
                        switches, focus, productivity, stress, sleep_, reels, youtube, chat, night):
    wellness = max(0.0, min(100.0,
        focus * 0.25 + productivity * 0.25 + (10 - stress) * 5
        + sleep_ * 3 + study * 2 - screen * 1.5 - gaming * 2 - reels * 3
    ))
    risk = min(100.0,
        screen * 3 + gaming * 4 + reels * 5 + night * 6
        + stress * 3 + (100 - focus) * 0.3
    )
    prod_idx = max(0.0, min(100.0,
        productivity * 0.4 + focus * 0.3 + study * 4 - screen * 1.2 - gaming * 2
    ))
    return round(wellness, 1), round(risk, 1), round(prod_idx, 1)


def _generate_insights(screen, gaming, social, reels, night, focus, productivity, sleep_, stress, study):
    tips = []
    if screen > 8:        tips.append("⚠️ Screen time exceeds 8hrs — digital fatigue risk detected")
    if gaming > 4:        tips.append("🎮 Gaming hours critically high — addiction pattern identified")
    if reels > 2:         tips.append("📱 Reels/shorts consumption affecting focus circuitry")
    if night > 2:         tips.append("🌙 Night usage disrupting circadian rhythm and sleep architecture")
    if focus < 40:        tips.append("🧠 Focus score critically low — context switching overload")
    if productivity < 40: tips.append("⚡ Productivity deficit detected — recommend deep work sessions")
    if sleep_ < 6:        tips.append("😴 Sleep deprivation detected — cognitive performance at risk")
    if stress > 7:        tips.append("🔴 Stress levels elevated — digital detox recommended")
    if study > 6:         tips.append("✅ Strong study/work pattern — maintain momentum")
    if social > 4:        tips.append("💬 Social media overconsumption pattern detected")
    return tips[:5] if tips else ["✅ Digital behavior within optimal parameters"]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/result')
def result():
    return render_template('result.html')


@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        body = request.get_json(silent=True) or {}

        def g(k, d=0.0): return float(body.get(k, d))

        screen      = g('screen_time')
        gaming      = g('gaming_hours')
        social      = g('social_media')
        ai_tools    = g('ai_tools')
        study       = g('study_hours')
        unlocks     = g('phone_unlocks')
        notifs      = g('notifications')
        switches    = g('app_switches')
        focus       = g('focus_score', 50)
        productivity= g('productivity_score', 50)
        stress      = g('stress_level', 5)
        sleep_      = g('sleep_hours', 7)
        reels       = g('reels_usage')
        youtube     = g('youtube_usage')
        chat        = g('chat_usage')
        night       = g('night_usage')

        vals_16 = [screen, gaming, social, ai_tools, study, unlocks, notifs, switches,
                   focus, productivity, stress, sleep_, reels, youtube, chat, night]

        X16 = _build_features_16(vals_16)
        X8  = _build_features_8(vals_16)

        # --- addiction model ---
        add_pred = _safe_predict(addiction_model, X16)
        if add_pred is None:
            add_pred = _safe_predict(addiction_model, X8)
        if add_pred is None:
            add_pred = 0

        add_proba_list = _safe_proba(addiction_model, X16, n_classes=len(BEHAVIOR_LABELS))
        if all(v == add_proba_list[0] for v in add_proba_list):
            add_proba_list = _safe_proba(addiction_model, X8, n_classes=len(BEHAVIOR_LABELS))
        add_prob = float(np.max(add_proba_list)) * 100

        # --- app classifier ---
        app_pred = _safe_predict(app_classifier, X16)
        if app_pred is None:
            app_pred = _safe_predict(app_classifier, X8)
        if app_pred is None:
            app_pred = 'Balanced'

        app_probs = _safe_proba(app_classifier, X16, n_classes=len(BEHAVIOR_LABELS))
        if all(v == app_probs[0] for v in app_probs):
            app_probs = _safe_proba(app_classifier, X8, n_classes=len(BEHAVIOR_LABELS))

        # --- trend model ---
        trend_pred = _safe_predict(trend_model, X8)
        if trend_pred is None:
            trend_pred = _safe_predict(trend_model, X16)
        if trend_pred is None:
            trend_pred = 1

        if isinstance(trend_pred, (int, np.integer)):
            trend_label = TREND_LABELS[int(trend_pred) % len(TREND_LABELS)]
        elif isinstance(trend_pred, str) and trend_pred in TREND_LABELS:
            trend_label = trend_pred
        else:
            try:
                trend_label = TREND_LABELS[int(float(str(trend_pred))) % len(TREND_LABELS)]
            except Exception:
                trend_label = 'Stable'

        # --- calc.exe ---
        calc_args = [screen, gaming, social, study, sleep_, stress, focus, productivity,
                     reels, youtube, chat, night, unlocks, notifs, switches, ai_tools]
        calc_data = _run_calc(calc_args)

        fb_wellness, fb_risk, fb_prod = _compute_fallbacks(
            screen, gaming, social, ai_tools, study, unlocks, notifs,
            switches, focus, productivity, stress, sleep_, reels, youtube, chat, night
        )

        wellness    = float(calc_data.get('wellness_score',    fb_wellness))
        risk_score  = float(calc_data.get('risk_score',        fb_risk))
        prod_idx    = float(calc_data.get('productivity_index', fb_prod))

        add_int = int(add_pred) if isinstance(add_pred, (int, float, np.integer, np.floating)) else 0

        return jsonify({
            'success': True,
            'addiction_prediction':  add_int,
            'addiction_probability': round(add_prob, 2),
            'app_category':          str(app_pred),
            'app_probabilities':     app_probs,
            'trend_prediction':      int(trend_pred) if isinstance(trend_pred, (int, np.integer)) else 1,
            'trend_label':           trend_label,
            'wellness_score':        round(wellness, 1),
            'risk_score':            round(risk_score, 1),
            'productivity_index':    round(prod_idx, 1),
            'behavior_label':        BEHAVIOR_LABELS[add_int % len(BEHAVIOR_LABELS)],
            'insights':              _generate_insights(screen, gaming, social, reels, night,
                                                        focus, productivity, sleep_, stress, study)
        })

    except Exception as e:
        app.logger.error(traceback.format_exc())
        return jsonify({'success': False, 'error': str(e)}), 500


@app.errorhandler(404)
def not_found(e):
    return jsonify({'success': False, 'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)