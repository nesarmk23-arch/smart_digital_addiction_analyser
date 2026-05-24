#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_FACTORS 10

typedef struct {
    char name[50];
    float value;
    float weight;
    float threshold;
} RiskFactor;

float compute_factor_risk(RiskFactor *f) {
    if (f->value <= f->threshold) return 0.0;
    float excess = f->value - f->threshold;
    return excess * f->weight;
}

float compute_total_risk(RiskFactor factors[], int n) {
    float total = 0.0;
    int i;
    for (i = 0; i < n; i++)
        total += compute_factor_risk(&factors[i]);
    if (total > 100) total = 100;
    return total;
}

void log_to_file(float screen, float gaming, float sleep, float social, float risk) {
    FILE *fp = fopen("risk_log.txt", "a");
    if (!fp) return;
    fprintf(fp, "screen=%.1f gaming=%.1f sleep=%.1f social=%.1f risk=%.2f\n",
            screen, gaming, sleep, social, risk);
    fclose(fp);
}

char *risk_label(float score) {
    if (score < 20) return "Minimal";
    if (score < 40) return "Low";
    if (score < 60) return "Moderate";
    if (score < 80) return "High";
    return "Critical";
}

int main(int argc, char *argv[]) {
    if (argc < 5) {
        printf("{\"error\":\"Insufficient arguments\"}");
        return 1;
    }
    float screen  = atof(argv[1]);
    float gaming  = atof(argv[2]);
    float sleep   = atof(argv[3]);
    float social  = atof(argv[4]);

    RiskFactor factors[4];
    strcpy(factors[0].name, "screen_time");
    factors[0].value = screen; factors[0].weight = 3.5; factors[0].threshold = 6.0;

    strcpy(factors[1].name, "gaming");
    factors[1].value = gaming; factors[1].weight = 5.0; factors[1].threshold = 2.0;

    strcpy(factors[2].name, "sleep_deficit");
    factors[2].value = (sleep < 7) ? (7 - sleep) : 0;
    factors[2].weight = 6.0; factors[2].threshold = 0.0;

    strcpy(factors[3].name, "social_media");
    factors[3].value = social; factors[3].weight = 3.0; factors[3].threshold = 2.0;

    float risk = compute_total_risk(factors, 4);
    log_to_file(screen, gaming, sleep, social, risk);
    printf("{\"risk_score\":%.2f,\"label\":\"%s\"}", risk, risk_label(risk));
    return 0;
}
