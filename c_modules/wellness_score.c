#include <stdio.h>
typedef struct
{
    float sleep;
    float study;
    float gaming;
    float social;
    float ai;
    float youtube;
} User;

float calculateWellness(User *u)
{
    float score = 100;

    score += u->sleep * 2;
    score += u->study * 3;
    score += u->ai * 1.5;

    score -= u->gaming * 4;
    score -= u->social * 3;
    score -= u->youtube * 2;

    if (score > 100)
        score = 100;
    if (score < 0)
        score = 0;

    return score;
}

int main(int argc, char *argv[])
{
    User u;

    u.sleep = atof(argv[1]);
    u.study = atof(argv[2]);
    u.gaming = atof(argv[3]);
    u.social = atof(argv[4]);
    u.ai = atof(argv[5]);
    u.youtube = atof(argv[6]);

    printf("{\"wellness_score\":%.2f}",
           calculateWellness(&u));

    return 0;
}