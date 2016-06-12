typedef struct {
  int p_id;
  wchar_t *p_name;
} board_t;

board_t *create(int id, const wchar_t *name);
void board_destroy(board_t *p);
