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
// FIXED SIZE
// =========================================

editor.setSize(

    "100%",

    "600px"
);


// =========================================
// AUTOSAVE
// =========================================

window.onload = () => {

    const saved = localStorage.getItem(
        "rcml_code"
    );

    if (saved) {

        editor.setValue(saved);
    }
};


editor.on("change", () => {

    localStorage.setItem(

        "rcml_code",

        editor.getValue()
    );
});


// =========================================
// INSERT COMMAND
// =========================================

function insertCommand(command) {

    editor.replaceSelection(

        command + "\n"
    );

    editor.focus();
}


// =========================================
// RUN CODE
// =========================================

async function runCode() {

    const code = editor.getValue();

    try {

        const response = await fetch(

            "/run",

            {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    code: code
                })
            }
        );

        const result = await response.json();

        // =====================================
        // ERROR
        // =====================================

        if (!result.success) {

            document.getElementById(
                "kuka_src"
            ).textContent = result.error;

            return;
        }

        // =====================================
        // KUKA SRC
        // =====================================

        if (result.kuka_src) {

            document.getElementById(
                "kuka_src_box"
            ).style.display = "block";

            document.getElementById(
                "kuka_src"
            ).textContent = result.kuka_src;

        } else {

            document.getElementById(
                "kuka_src_box"
            ).style.display = "none";
        }

        // =====================================
        // KUKA DAT
        // =====================================

        if (result.kuka_dat) {

            document.getElementById(
                "kuka_dat_box"
            ).style.display = "block";

            document.getElementById(
                "kuka_dat"
            ).textContent = result.kuka_dat;

        } else {

            document.getElementById(
                "kuka_dat_box"
            ).style.display = "none";
        }

        // =====================================
        // UR
        // =====================================

        if (result.ur_script) {

            document.getElementById(
                "ur_box"
            ).style.display = "block";

            document.getElementById(
                "ur_output"
            ).textContent = result.ur_script;

        } else {

            document.getElementById(
                "ur_box"
            ).style.display = "none";
        }

    }

    catch (error) {

        document.getElementById(
            "kuka_src_box"
        ).style.display = "block";

        document.getElementById(
            "kuka_src"
        ).textContent = error;
    }
}

// =========================================
// SIMULATE
// =========================================

async function simulateCode() {

    try {

        const code = editor.getValue();

        const response = await fetch(

            "/simulate",

            {

                method: "POST",

                headers: {

                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    code: code
                })
            }
        );

        const result = await response.json();

        if (!result.success) {

            alert(result.error);

            return;
        }

        alert(

            "RoboDK simulation started"
        );

    }

    catch (error) {

        console.error(error);

        alert(error);
    }
}

// =========================================
// SAVE RCML
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
// LOAD RCML
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


// =========================================
// SAVE GENERATED OUTPUT
// =========================================

function saveOutput(

    elementId,

    filename

) {

    const text = document.getElementById(

        elementId

    ).textContent;

    const blob = new Blob(

        [text],

        {
            type: "text/plain"
        }
    );

    const a = document.createElement("a");

    a.href = URL.createObjectURL(blob);

    a.download = filename;

    a.click();
}