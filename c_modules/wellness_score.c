#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    float screen_time;
    float gaming;
    float sleep;
    float social_media;
} UserData;

float calculate_wellness(UserData *u) {
    float score = 100.0;
    if (u->screen_time > 8) score -= (u->screen_time - 8) * 5;
    if (u->gaming > 3)      score -= (u->gaming - 3) * 6;
    if (u->sleep < 7)       score -= (7 - u->sleep) * 8;
    if (u->social_media > 3) score -= (u->social_media - 3) * 4;
    if (score < 0) score = 0;
    if (score > 100) score = 100;
    return score;
}

char *wellness_label(float score) {
    if (score >= 80) return "Excellent";
    if (score >= 60) return "Good";
    if (score >= 40) return "Fair";
    if (score >= 20) return "Poor";
    return "Critical";
}

int main(int argc, char *argv[]) {
    if (argc < 5) {
        printf("{\"error\":\"Insufficient arguments\"}");
        return 1;
    }
    UserData u;
    u.screen_time  = atof(argv[1]);
    u.gaming       = atof(argv[2]);
    u.sleep        = atof(argv[3]);
    u.social_media = atof(argv[4]);
    float score = calculate_wellness(&u);
    printf("{\"wellness_score\":%.2f,\"label\":\"%s\"}", score, wellness_label(score));
    return 0;
}
