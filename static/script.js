// =========================================
// RCML MODE
// =========================================

CodeMirror.defineSimpleMode("rcml", {

    start: [

        {
            regex: /\b(robot|point|task|parallel|sync|wait)\b/,
            token: "keyword"
        },

        {
            regex: /\b(kuka|ur)\b/,
            token: "variable-2"
        },

        {
            regex: /\b(move|grab|release|home)\b/,
            token: "def"
        },

        {
            regex: /\b\d+\b/,
            token: "number"
        },

        {
            regex: /#.*/,
            token: "comment"
        }
    ]
});


// =========================================
// EDITOR
// =========================================

const editor = CodeMirror.fromTextArea(

    document.getElementById("code"),

    {

        mode: "rcml",

        theme: "dracula",

        lineNumbers: true,

        indentUnit: 4,

        tabSize: 4,

        placeholder:
            "Write your RCML code here..."
    }
);


// =========================================
// LOAD SAVED CODE
// =========================================

window.onload = () => {

    const saved = localStorage.getItem(
        "rcml_code"
    );

    if (saved) {

        editor.setValue(saved);
    }
};


// =========================================
// AUTOSAVE
// =========================================

editor.on("change", () => {

    localStorage.setItem(

        "rcml_code",

        editor.getValue()
    );
});


// =========================================
// SAVE FILE
// =========================================

function saveFile() {

    const code = editor.getValue();

    const blob = new Blob(

        [code],

        {
            type: "text/plain"
        }
    );

    const a = document.createElement("a");

    a.href = URL.createObjectURL(blob);

    a.download = "program.rcml";

    a.click();
}


// =========================================
// LOAD FILE
// =========================================

function loadFile() {

    const input = document.getElementById(
        "fileInput"
    );

    input.click();

    input.onchange = e => {

        const file = e.target.files[0];

        if (!file) {
            return;
        }

        const reader = new FileReader();

        reader.onload = event => {

            editor.setValue(
                event.target.result
            );
        };

        reader.readAsText(file);
    };
}