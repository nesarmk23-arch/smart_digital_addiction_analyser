#include <stdio.h>
#include <stdlib.h>

typedef struct Node
{
    float value;
    struct Node *next;
} Node;

Node *createNode(float value)
{
    Node *temp =
        (Node *)malloc(sizeof(Node));

    temp->value = value;
    temp->next = NULL;

    return temp;
}

float calculateProductivity(Node *head)
{
    float score = 0;

    while (head)
    {
        score += head->value;
        head = head->next;
    }

    if (score > 100)
        score = 100;

    return score;
}

int main(int argc, char *argv[])
{
    float study = atof(argv[1]);
    float sleep = atof(argv[2]);
    float ai = atof(argv[3]);

    Node *head = createNode(study * 8);

    head->next = createNode(sleep * 4);

    head->next->next =
        createNode(ai * 3);

    float score =
        calculateProductivity(head);

    printf("{\"productivity_score\":%.2f}",
           score);

    return 0;
}