document.addEventListener("DOMContentLoaded", function () {
  const articleContent = document.querySelector('textarea[name="content"]');

  // articleContent &&
  let mde = new SimpleMDE({
    element: articleContent,
    previewRender: function (plainText, preview) {
      // 自定義圖片寬度語法: ![alt](src){width-50}
      const customImageSyntax = /!\[([^\]]*)\]\(([^)]+)\)\{width-(\d+)\}/g;
      let html = plainText.replace(
        customImageSyntax,
        function (match, alt, src, width) {
          // 加入br是為了讓圖片跟上下文字有間距
          return (
            '<br /><img src="' +
            src +
            '" alt="' +
            alt +
            '" style="width: ' +
            width +
            '%; height: auto;"><br/>'
          );
        }
      );

      html = this.parent.markdown(html);
      // 需要將table上下加上<br>，否則會太擠
      html = html.replace(/<table>/g, "<br /><table>");
      html = html.replace(/<\/table>/g, "</table><br />");

      // 添加自定義 CSS
      const customCSS = `
		  <style>
			/* 在這裡添加您的自定義 CSS */
			table {
			  width: 100%;
			  border-collapse: collapse;
			}
			/* 添加更多自定義樣式... */
		  </style>
		`;

      // 將 HTML 包裝在具有自定義類的 div 中，並添加自定義 CSS
      return customCSS + '<div class="custom-preview">' + html + "</div>";
    },
    spellChecker: false,
    toolbar: [
      "bold",
      "italic",
      "heading",
      "|",
      "quote",
      "unordered-list",
      "ordered-list",
      "|",
      "link",
      {
        name: "table",
        action: drawTable,
        className: "fa fa-table",
        title: "Insert Table",
      },
      {
        name: "image",
        action: function customFunction(editor) {
          uploadImage(editor);
        },
        className: "fa fa-picture-o",
        title: "Upload Image",
      },
      "|",
      "preview",
      "side-by-side",
      "fullscreen",
    ],
  });

  function uploadImage(editor) {
    const inputFile = document.createElement("input");
    inputFile.type = "file";
    inputFile.accept = "image/*";
    inputFile.onchange = function () {
      let file = this.files[0];
      let formData = new FormData();
      formData.append("image", file);

      fetch("/article/upload_image/", {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            let imageUrl = data.url;
            let mdEditor = editor.codemirror;
            let output = "![" + file.name + "](" + imageUrl + "){width-50}";
            mdEditor.replaceSelection(output);
          } else {
            console.error("Upload failed");
            alert("Image upload failed. Please try again.");
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          alert("An error occurred during upload. Please try again.");
        });
    };
    inputFile.click();
  }

  function drawTable(editor) {
    const cm = editor.codemirror;
    const output =
      "\n| Column 1 | Column 2 | Column 3 |\n" +
      "| --- | --- | --- |\n" +
      "| Text     | Text     | Text     |\n" +
      "| Text     | Text     | Text     |\n";
    cm.replaceSelection(output);
  }
});
