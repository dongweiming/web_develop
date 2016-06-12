require(["base/js/events", "base/js/namespace", "notebook/js/cell",
         "codemirror/lib/codemirror", "codemirror/keymap/emacs"],
        function(events, Jupyter, Cell, CodeMirror) {
            events.on('notebook_loaded.Notebook', function(){
                var load_ipython_extension = function() {
                    var extraKeys = CodeMirror.keyMap.emacs;
                    Cell.Cell.options_default.cm_config.extraKeys = extraKeys;
                    Cell.Cell.options_default.cm_config.lineWrapping = true;

                    var cells = Jupyter.notebook.get_cells();
                    var numCells = cells.length;
                    for (var i = 0; i < numCells; i++) {
                        var theseExtraKeys = cells[i].code_mirror.getOption('extraKeys');
                        for (var k in extraKeys) {
                            theseExtraKeys[k] = extraKeys[k];
                        }
                        cells[i].code_mirror.setOption('extraKeys', theseExtraKeys);
                        cells[i].code_mirror.setOption('lineWrapping', true);
                    }

                    // exentensions from IPython-notebook-extensions
                    Jupyter.load_extensions('usability/chrome_clipboard');
                    Jupyter.load_extensions('usability/dragdrop/drag-and-drop');
                };

                return {
                    load_ipython_extension: load_ipython_extension,
                };
            });
        });
