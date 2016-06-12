#include <stdlib.h>
#include <wchar.h>

board_t *create(int id, const wchar_t *name) {
  board_t *p = malloc(sizeof(board_t));
  if (!p)
    return NULL;
  p->p_id = id;
  p->p_name = wcsdup(name);
  return p;
}

void board_destroy(board_t *p) {
  if (p->p_name)
    free(p->p_name);
  free(p);
}
