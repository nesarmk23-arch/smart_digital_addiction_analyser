#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Node {
    float value;
    struct Node *next;
} Node;

Node *create_node(float val) {
    Node *n = (Node *)malloc(sizeof(Node));
    n->value = val;
    n->next = NULL;
    return n;
}

float sum_list(Node *head) {
    float total = 0;
    Node *cur = head;
    while (cur) { total += cur->value; cur = cur->next; }
    return total;
}

void free_list(Node *head) {
    Node *cur = head;
    while (cur) { Node *tmp = cur->next; free(cur); cur = tmp; }
}

float calc_productive_hours(float screen, float gaming, float social, float sleep) {
    Node *head = create_node(screen);
    head->next = create_node(gaming);
    head->next->next = create_node(social);
    float waste = sum_list(head);
    free_list(head);
    float awake = 24.0 - sleep;
    float productive = awake - waste;
    if (productive < 0) productive = 0;
    return productive;
}

float calc_productivity_score(float screen, float gaming, float social, float sleep) {
    float productive = calc_productive_hours(screen, gaming, social, sleep);
    float awake = 24.0 - sleep;
    if (awake <= 0) return 0;
    float score = (productive / awake) * 100.0;
    if (score > 100) score = 100;
    return score;
}

char *productivity_label(float score) {
    if (score >= 75) return "Highly Productive";
    if (score >= 50) return "Moderately Productive";
    if (score >= 25) return "Low Productivity";
    return "Unproductive";
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
    float productive = calc_productive_hours(screen, gaming, social, sleep);
    float score   = calc_productivity_score(screen, gaming, social, sleep);
    printf("{\"productivity_score\":%.2f,\"productive_hours\":%.2f,\"label\":\"%s\"}",
           score, productive, productivity_label(score));
    return 0;
}
