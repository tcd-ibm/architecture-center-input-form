import { useState } from 'react';
import Editor from 'react-simple-code-editor';
import { highlight, languages } from 'prismjs/components/prism-core';
import 'prismjs/components/prism-asciidoc';
import Asciidoctor from 'asciidoctor';

// eslint-disable-next-line custom-rules/no-global-css
import 'prismjs/themes/prism.css';

// eslint-disable-next-line custom-rules/no-global-css
import './asciidocEditor.scss';


const asciidoctor = Asciidoctor();

const hightlightWithLineNumbers = (input, language) =>
  highlight(input, language)
    .split('\n')
    .map((line, i) => `<span class='lineNumber'>${i + 1}</span>${line}`)
    .join('\n');

function DocEditor() {

  const [code, setCode] = useState(
    'This is an interactive editor.\nUse it to try https://asciidoc.org[AsciiDoc].\n\n== Section Title\n\n* A list item\n* Another list item'
  );

  return (
    <>
      <div className='container'>
        <div className='editorContainer'>
          <Editor
            value={code}
            onValueChange={code => setCode(code)}
            highlight={code => hightlightWithLineNumbers(code, languages.asciidoc)}
            className='editor'
            textareaId='codeArea'
            style={{
              fontFamily: '"Fira code", "Fira Mono", monospace',
              fontSize: 12,
            }}
          />
        </div>
        <div className='separator'></div>
        <div className='previewContainer' dangerouslySetInnerHTML={{ __html: asciidoctor.convert(code) }}>
        </div>
      </div>
    </>
  );
}

export default DocEditor;