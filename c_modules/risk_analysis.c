#include <stdio.h>
#include <stdlib.h>

typedef struct
{
    char factor[30];
    float value;
    float weight;
} RiskFactor;

float calculateRisk(RiskFactor r[], int n)
{
    float risk = 0;

    for (int i = 0; i < n; i++)
    {
        risk += r[i].value * r[i].weight;
    }

    if (risk > 100)
        risk = 100;

    return risk;
}

int main(int argc, char *argv[])
{
    if (argc != 6)
    {
        printf("Usage: risk_analysis <gaming> <social> <youtube> <notifications> <unlocks>\n");
        return 1;
    }

    RiskFactor r[5];

    r[0].value = atof(argv[1]);
    r[0].weight = 5;

    r[1].value = atof(argv[2]);
    r[1].weight = 4;

    r[2].value = atof(argv[3]);
    r[2].weight = 3;

    r[3].value = atof(argv[4]);
    r[3].weight = 0.1;

    r[4].value = atof(argv[5]);
    r[4].weight = 0.2;

    float risk = calculateRisk(r, 5);

    FILE *fp = fopen("risk_log.txt", "a");

    if (fp != NULL)
    {
        fprintf(fp, "Risk Score = %.2f\n", risk);
        fclose(fp);
    }

    printf("{\"risk_score\":%.2f}", risk);

    return 0;
}