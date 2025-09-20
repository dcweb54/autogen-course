

playwright codegen https://playwright.dev/


playwright codegen --target python-async https://playwright.dev/


const button = await document.querySelector('colab-run-button')
const executionDiv = button.shadowRoot.querySelector('.cell-execution');

const output = document.querySelector('div[class="codecell-input-output"]  div[class="output"] div[class="output-content"] div[class="output-iframe-container"]').textContent.trim().split("\n")

console.log({
    isRunning: executionDiv.classList.contains('running') || 
              executionDiv.classList.contains('animating'),
    isFocused: executionDiv.classList.contains('focused'),
    hasError: executionDiv.classList.contains('error') || 
             executionDiv.querySelector('.error') !== null,
    ouput:output
});


async function getColabExecutionStatus() {
  try {
    // 1. Find the run button
    const button = document.querySelector('colab-run-button');
    if (!button) {
      throw new Error('Colab run button not found. Make sure you are in a Colab notebook environment.');
    }

    // 2. Access shadow DOM (may not be available immediately)
    const shadowRoot = button.shadowRoot;
    if (!shadowRoot) {
      throw new Error('Shadow DOM not available. Button might not be fully loaded.');
    }

    // 3. Find execution status div
    const executionDiv = shadowRoot.querySelector('.cell-execution');
    if (!executionDiv) {
      throw new Error('Execution status div (.cell-execution) not found inside shadow root.');
    }

    // 4. Extract output content (optional — may not exist if cell hasn’t run)
    let output = [];
    const outputContainer = document.querySelector(
      'div.codecell-input-output div.output div.output-content div.output-iframe-container'
    );

    if (outputContainer && outputContainer.textContent) {
      output = outputContainer.textContent.trim().split('\n');
    } else {
      console.warn('Output container not found or empty. Cell may not have executed yet.');
    }

    // 5. Build and return structured result
    return {
      success: true,
      data: {
        isRunning: executionDiv.classList.contains('running') || executionDiv.classList.contains('animating'),
        isFocused: executionDiv.classList.contains('focused'),
        hasError: executionDiv.classList.contains('error') || !!executionDiv.querySelector('.error'),
        output: output // Note: corrected typo from "ouput" → "output"
      }
    };

  } catch (error) {
    console.error('Error in getColabExecutionStatus:', error.message);
    return {
      success: false,
      error: error.message,
      data: null
    };
  }
}

div[class="codecell-input-output"]  div[class="output"] div[class="output-content"] div[class="output-iframe-container"]




// handle click


document.querySelector('div[class="codecell-input-output"] div[class="cell-gutter"] div[class="cell-execution-container"] colab-run-button[class="cell-ui-refresh"]').click()


<!--  click the cell -->
<!-- runining the cell finished -->
<!-- show restart -->
<!-- click the restart button -->


['t3_23lang.safetensors:  97% 2.09G/2.14G [00:18<00:00, 233MB/s]', '', 't3_23lang.safetensors:  99% 2.12G/2.14G [00:18<00:00, 241MB/s]', '', 't3_23lang.safetensors: 100% 2.14G/2.14G [00:18<00:00, 115MB/s]', 'Fetching 6 files: 100% 6/6 [00:18<00:00,  3.14s/it]', '/usr/local/lib/python3.12/dist-packages/diffusers/models/lora.py:393: FutureWarning: `LoRACompatibleLinear` is deprecated and will be removed in version 1.0.0. Use of `LoRACompatibleLinear` is deprecated. Please switch to PEFT backend by installing PEFT: `pip install peft`.', '  deprecate("LoRACompatibleLinear", "1.0.0", deprecation_message)', 'Cangjie5_TC.json: 1.92MB [00:00, 4.87MB/s]', 'WARNING:src.chatterbox.models.tokenizers.tokenizer:pkuseg not available - Chinese segmentation will be skipped', 'loaded PerthNet (Implicit) at step 250,000', 'Model loaded successfully. Internal device: cuda', '* Running on local URL:  http://127.0.0.1:7860', '* Running on public URL: https://2aef41db01a16f3802.gradio.live', '', 'This share link expires in 1 week. For free permanent hosting and GPU upgrades, run `gradio deploy` from the terminal in the working directory to deploy to Hugging Face Spaces (https://huggingface.co/spaces)', 'Keyboard interruption in main thread... closing server.', '^C']

// for reference
<div class="codecell-input-output">
      <div class="inputarea horizontal layout code">
        <div class="cell-gutter">
          <!-- Bounding range for vertical scrolling of icons -->
          <div class="cell-execution-container">
            <colab-run-button class="cell-ui-refresh"></colab-run-button>
          </div>
        </div>
      <div class="editor flex lazy-editor" style=""><div class="editor flex monaco" data-keybinding-context="3" data-mode-id="notebook-python" style="height: 143px; --vscode-editorCodeLens-lineHeight: 16px; --vscode-editorCodeLens-fontSize: 12px; --vscode-editorCodeLens-fontFeatureSettings: &quot;liga&quot; off, &quot;calt&quot; off;"><div class="monaco-editor no-user-select  showUnused showDeprecated vs-dark" role="code" data-uri="inmemory://model/3" style="width: 1205px; height: 143px;"><div data-mprt="3" class="overflow-guard" style="width: 1205px; height: 143px; overflow: clip;"><div class="margin" role="presentation" aria-hidden="true" style="position: absolute; contain: strict; will-change: unset; top: 0px; height: 143px; width: 40px;"><div class="glyph-margin" style="left: 0px; width: 19px; height: 143px;"></div><div class="margin-view-zones" role="presentation" aria-hidden="true" style="position: absolute;"></div><div class="margin-view-overlays" role="presentation" aria-hidden="true" style="position: absolute; font-family: monospace, Consolas, &quot;Courier New&quot;, monospace; font-weight: normal; font-size: 14px; font-feature-settings: &quot;liga&quot; 0, &quot;calt&quot; 0; font-variation-settings: normal; line-height: 19px; letter-spacing: 0px; width: 40px; height: 143px;"><div style="position:absolute;top:0px;width:100%;height:19px;"><div class="line-numbers" style="left:19px;width:15px;">1</div></div><div style="position:absolute;top:19px;width:100%;height:19px;"><div class="line-numbers" style="left:19px;width:15px;">2</div></div><div style="position:absolute;top:38px;width:100%;height:19px;"><div class="line-numbers" style="left:19px;width:15px;">3</div></div><div style="position:absolute;top:57px;width:100%;height:19px;"><div class="line-numbers" style="left:19px;width:15px;">4</div></div><div style="position:absolute;top:76px;width:100%;height:19px;"><div class="line-numbers" style="left:19px;width:15px;">5</div></div><div style="position:absolute;top:95px;width:100%;height:19px;"><div class="line-numbers" style="left:19px;width:15px;">6</div></div><div style="position:absolute;top:114px;width:100%;height:19px;"><div class="current-line current-line-margin-both" style="width:40px; height:19px;"></div><div class="line-numbers active-line-number" style="left:19px;width:15px;">7</div></div></div><div class="glyph-margin-widgets" style="position: absolute; top: 0px;"></div></div><div class="monaco-scrollable-element editor-scrollable vs-dark" role="presentation" data-mprt="5" style="position: absolute; overflow: hidden; left: 40px; width: 1165px; height: 143px;"><div class="lines-content monaco-editor-background" style="position: absolute; overflow: hidden; width: 1e+06px; height: 143px; contain: strict; will-change: unset; top: 0px; left: 0px;"><div class="view-overlays" role="presentation" aria-hidden="true" style="position: absolute; font-family: monospace, Consolas, &quot;Courier New&quot;, monospace; font-weight: normal; font-size: 14px; font-feature-settings: &quot;liga&quot; 0, &quot;calt&quot; 0; font-variation-settings: normal; line-height: 19px; letter-spacing: 0px; height: 0px; width: 1165px;"><div style="position:absolute;top:0px;width:100%;height:19px;"></div><div style="position:absolute;top:19px;width:100%;height:19px;"></div><div style="position:absolute;top:38px;width:100%;height:19px;"></div><div style="position:absolute;top:57px;width:100%;height:19px;"></div><div style="position:absolute;top:76px;width:100%;height:19px;"></div><div style="position:absolute;top:95px;width:100%;height:19px;"></div><div style="position:absolute;top:114px;width:100%;height:19px;"><div class="current-line" style="width:1165px; height:19px;"></div></div></div><div role="presentation" aria-hidden="true" class="view-rulers"></div><div class="view-zones" role="presentation" aria-hidden="true" style="position: absolute;"></div><div class="view-lines monaco-mouse-cursor-text" role="presentation" aria-hidden="true" data-mprt="7" style="position: absolute; font-family: monospace, Consolas, &quot;Courier New&quot;, monospace; font-weight: normal; font-size: 14px; font-feature-settings: &quot;liga&quot; 0, &quot;calt&quot; 0; font-variation-settings: normal; line-height: 19px; letter-spacing: 0px; width: 1165px; height: 143px;"><div style="top:0px;height:19px;" class="view-line"><span><span class="mtk20">import</span><span class="mtk1">&nbsp;asyncio</span></span></div><div style="top:19px;height:19px;" class="view-line"><span><span></span></span></div><div style="top:38px;height:19px;" class="view-line"><span><span class="mtk20">await</span><span class="mtk1">&nbsp;asyncio.sleep</span><span class="mtk14 bracket-highlighting-0">(</span><span class="mtk6">30</span><span class="mtk14 bracket-highlighting-0">)</span></span></div><div style="top:57px;height:19px;" class="view-line"><span><span class="mtk17">print</span><span class="mtk14 bracket-highlighting-0">(</span><span class="mtk5">"welcome"</span><span class="mtk14 bracket-highlighting-0">)</span></span></div><div style="top:76px;height:19px;" class="view-line"><span><span></span></span></div><div style="top:95px;height:19px;" class="view-line"><span><span class="mtk20">await</span><span class="mtk1">&nbsp;asyncio.sleep</span><span class="mtk14 bracket-highlighting-0">(</span><span class="mtk6">30</span><span class="mtk14 bracket-highlighting-0">)</span></span></div><div style="top:114px;height:19px;" class="view-line"><span><span class="mtk17">print</span><span class="mtk14 bracket-highlighting-0">(</span><span class="mtk5">"how&nbsp;to&nbsp;make&nbsp;code"</span><span class="mtk14 bracket-highlighting-0">)</span></span></div></div><div data-mprt="1" class="contentWidgets" style="position: absolute; top: 0px;"><div class="lightBulbWidget codicon-light-bulb codicon" widgetid="LightBulbWidget" title="Show Code Actions (Ctrl+.)" style="position: absolute; display: none; visibility: hidden; max-width: 1165px; top: 38px; left: 0px;"></div></div><div role="presentation" aria-hidden="true" class="cursors-layer cursor-line-style cursor-solid"><div class="cursor monaco-mouse-cursor-text " style="height: 19px; top: 114px; left: 176px; font-family: monospace, Consolas, &quot;Courier New&quot;, monospace; font-weight: normal; font-size: 14px; font-feature-settings: &quot;liga&quot; 0, &quot;calt&quot; 0; font-variation-settings: normal; line-height: 19px; letter-spacing: 0px; display: block; visibility: hidden; padding-left: 1px; width: 2px;"></div></div></div><div role="presentation" aria-hidden="true" class="invisible scrollbar horizontal" style="position: absolute; width: 1151px; height: 10px; left: 0px; bottom: 0px;"><div class="slider" style="position: absolute; top: 0px; left: 0px; height: 10px; transform: translate3d(0px, 0px, 0px); contain: strict; will-change: unset; width: 1151px;"></div></div><canvas class="decorationsOverviewRuler" aria-hidden="true" width="14" height="143" style="position: absolute; transform: translate3d(0px, 0px, 0px); contain: strict; top: 0px; right: 0px; width: 14px; height: 143px; will-change: unset; display: block;"></canvas><div role="presentation" aria-hidden="true" class="invisible scrollbar vertical" style="position: absolute; width: 14px; height: 143px; right: 0px; top: 0px;"><div class="slider" style="position: absolute; top: 0px; left: 0px; width: 14px; transform: translate3d(0px, 0px, 0px); contain: strict; will-change: unset; height: 143px;"></div></div></div><div role="presentation" aria-hidden="true" style="width: 1205px;"></div><textarea data-mprt="6" class="inputarea monaco-mouse-cursor-text" wrap="on" autocorrect="off" autocapitalize="off" autocomplete="off" spellcheck="false" aria-label="Editor content;Press Alt+F1 for Accessibility Options." tabindex="0" role="textbox" aria-roledescription="editor" aria-multiline="true" aria-haspopup="false" aria-autocomplete="both" style="tab-size: 15.3984px; font-family: monospace, Consolas, &quot;Courier New&quot;, monospace; font-weight: normal; font-size: 14px; font-feature-settings: &quot;liga&quot; 0, &quot;calt&quot; 0; font-variation-settings: normal; line-height: 19px; letter-spacing: 0px; top: 114px; left: 40px; width: 76992px; height: 1px;"></textarea><div class="monaco-editor-background textAreaCover margin" style="position: absolute; top: 0px; left: 0px; width: 0px; height: 0px;"></div><div data-mprt="4" class="overlayWidgets" style="width: 1205px;"><div class="monaco-hover hidden" tabindex="0" role="tooltip" widgetid="editor.contrib.modesGlyphHoverWidget" style="position: absolute;"><div class="monaco-scrollable-element " role="presentation" style="position: relative; overflow: hidden;"><div class="monaco-hover-content" style="overflow: hidden;"></div><div role="presentation" aria-hidden="true" class="invisible scrollbar horizontal" style="position: absolute;"><div class="slider" style="position: absolute; top: 0px; left: 0px; height: 10px; transform: translate3d(0px, 0px, 0px); contain: strict;"></div></div><div role="presentation" aria-hidden="true" class="invisible scrollbar vertical" style="position: absolute;"><div class="slider" style="position: absolute; top: 0px; left: 0px; width: 10px; transform: translate3d(0px, 0px, 0px); contain: strict;"></div></div><div class="shadow"></div><div class="shadow"></div><div class="shadow"></div></div></div></div><div data-mprt="8" class="minimap slider-mouseover" role="presentation" aria-hidden="true" style="position: absolute; left: 0px; width: 0px; height: 143px;"><div class="minimap-shadow-hidden" style="height: 143px;"></div><canvas width="0" height="143" style="position: absolute; left: 0px; width: 0px; height: 143px;"></canvas><canvas class="minimap-decorations-layer" width="0" height="143" style="position: absolute; left: 0px; width: 0px; height: 143px;"></canvas><div class="minimap-slider" style="position: absolute; transform: translate3d(0px, 0px, 0px); contain: strict; width: 0px; will-change: unset;"><div class="minimap-slider-horizontal" style="position: absolute; width: 0px; height: 0px;"></div></div></div><div role="presentation" aria-hidden="true" class="blockDecorations-container"></div></div><div data-mprt="2" class="overflowingContentWidgets" style="display: none;"><div widgetid="editor.contrib.resizableContentHoverWidget" style="position: fixed; height: 10px; width: 10px; z-index: 50; display: none; visibility: hidden; max-width: 1366px; top: 254px; left: 245px;"><div class="monaco-sash vertical" style="left: 8px;"></div><div class="monaco-sash vertical disabled" style="left: -2px;"></div><div class="monaco-sash orthogonal-edge-north horizontal" style="top: -2px;"><div class="orthogonal-drag-handle end"></div></div><div class="monaco-sash orthogonal-edge-south horizontal disabled" style="top: 8px;"><div class="orthogonal-drag-handle end"></div></div><div class="monaco-hover hidden" tabindex="0" role="tooltip" style="width: 0px; height: 0px;"><div class="monaco-scrollable-element " role="presentation" style="position: relative; overflow: hidden;"><div class="monaco-hover-content" style="overflow: hidden; font-size: 14px; line-height: 1.35714; max-width: 795.3px; max-height: 250px; width: 0px; height: 0px;"><div class="hover-row markdown-hover"><div class="hover-contents"><div class="rendered-markdown"><p><code>int: count</code></p></div></div></div><div class="hover-row markdown-hover"><div class="hover-contents"><div class="rendered-markdown"><p><code>30</code></p></div></div></div></div><div role="presentation" aria-hidden="true" class="invisible scrollbar horizontal" style="position: absolute; width: 0px; height: 10px; left: 0px; bottom: 0px;"><div class="slider" style="position: absolute; top: 0px; left: 0px; height: 10px; transform: translate3d(0px, 0px, 0px); contain: strict; width: 0px;"></div></div><div role="presentation" aria-hidden="true" class="invisible scrollbar vertical" style="position: absolute; width: 10px; height: 0px; right: 0px; top: 0px;"><div class="slider" style="position: absolute; top: 0px; left: 0px; width: 10px; transform: translate3d(0px, 0px, 0px); contain: strict; height: 0px;"></div></div><div class="shadow"></div><div class="shadow"></div><div class="shadow"></div></div></div></div><div class="editor-widget suggest-widget" widgetid="editor.widget.suggestWidget" style="position: fixed; display: none; visibility: hidden; max-width: 1366px; height: 59px; width: 430px; top: 216px; left: 215px;"><div class="monaco-sash vertical" style="left: 428px;"></div><div class="monaco-sash vertical disabled" style="left: -2px;"></div><div class="monaco-sash orthogonal-edge-north horizontal disabled" style="top: -2px;"><div class="orthogonal-drag-handle end"></div></div><div class="monaco-sash orthogonal-edge-south horizontal" style="top: 57px;"><div class="orthogonal-drag-handle end"></div></div><div class="message" aria-hidden="true" style="display: none;"></div><div class="tree" style="height: 59px; display: none;" aria-hidden="true"><div class="monaco-list list_id_3 selection-none" tabindex="0" role="listbox" aria-label="Suggest"><div class="monaco-scrollable-element " role="presentation" style="position: relative; overflow: hidden;"><div class="monaco-list-rows" style="transform: translate3d(0px, 0px, 0px); overflow: hidden; contain: strict; height: 0px; left: 0px; top: 0px;"></div><div role="presentation" aria-hidden="true" class="invisible scrollbar horizontal" style="position: absolute; width: 0px; height: 10px; left: 0px; bottom: 0px;"><div class="slider" style="position: absolute; top: 0px; left: 0px; height: 10px; transform: translate3d(0px, 0px, 0px); contain: strict; width: 0px;"></div></div><div role="presentation" aria-hidden="true" class="invisible scrollbar vertical" style="position: absolute; width: 10px; height: 59px; right: 0px; top: 0px;"><div class="slider" style="position: absolute; top: 0px; left: 0px; width: 10px; transform: translate3d(0px, 0px, 0px); contain: strict; height: 59px;"></div></div></div><style type="text/css" media="screen">.monaco-list.list_id_3:focus .monaco-list-row.focused { background-color: var(--vscode-list-focusBackground); }
.monaco-list.list_id_3:focus .monaco-list-row.focused:hover { background-color: var(--vscode-list-focusBackground); }
.monaco-list.list_id_3:focus .monaco-list-row.focused { color: var(--vscode-list-focusForeground); }
.monaco-list.list_id_3:focus .monaco-list-row.selected { background-color: var(--vscode-list-activeSelectionBackground); }
.monaco-list.list_id_3:focus .monaco-list-row.selected:hover { background-color: var(--vscode-list-activeSelectionBackground); }
.monaco-list.list_id_3:focus .monaco-list-row.selected { color: var(--vscode-list-activeSelectionForeground); }
.monaco-list.list_id_3:focus .monaco-list-row.selected .codicon { color: var(--vscode-list-activeSelectionIconForeground); }

				.monaco-drag-image,
				.monaco-list.list_id_3:focus .monaco-list-row.selected.focused { background-color: var(--vscode-list-activeSelectionBackground); }
			

				.monaco-drag-image,
				.monaco-list.list_id_3:focus .monaco-list-row.selected.focused { color: var(--vscode-list-activeSelectionForeground); }
			
.monaco-list.list_id_3 .monaco-list-row.focused .codicon { color:  var(--vscode-list-inactiveSelectionIconForeground); }
.monaco-list.list_id_3 .monaco-list-row.focused { background-color:  var(--vscode-editorSuggestWidget-selectedBackground); }
.monaco-list.list_id_3 .monaco-list-row.focused:hover { background-color:  var(--vscode-editorSuggestWidget-selectedBackground); }
.monaco-list.list_id_3 .monaco-list-row.selected { background-color:  var(--vscode-list-inactiveSelectionBackground); }
.monaco-list.list_id_3 .monaco-list-row.selected:hover { background-color:  var(--vscode-list-inactiveSelectionBackground); }
.monaco-list.list_id_3 .monaco-list-row.selected { color: var(--vscode-list-inactiveSelectionForeground); }
.monaco-list.list_id_3:not(.drop-target):not(.dragging) .monaco-list-row:hover:not(.selected):not(.focused) { background-color: var(--vscode-list-hoverBackground); }
.monaco-list.list_id_3:not(.drop-target):not(.dragging) .monaco-list-row:hover:not(.selected):not(.focused) { color:  var(--vscode-list-hoverForeground); }
.monaco-list.list_id_3:focus .monaco-list-row.focused.selected { outline: 1px solid var(--vscode-list-focusAndSelectionOutline, var(--vscode-contrastActiveBorder, var(--vscode-list-focusOutline))); outline-offset: -1px;}

				.monaco-drag-image,
				.monaco-list.list_id_3:focus .monaco-list-row.focused { outline: 1px solid var(--vscode-list-focusOutline); outline-offset: -1px; }
				.monaco-workbench.context-menu-visible .monaco-list.list_id_3.last-focused .monaco-list-row.focused { outline: 1px solid var(--vscode-list-focusOutline); outline-offset: -1px; }
			
.monaco-list.list_id_3 .monaco-list-row.focused.selected { outline: 1px dotted var(--vscode-contrastActiveBorder, var(--vscode-contrastActiveBorder)); outline-offset: -1px; }
.monaco-list.list_id_3 .monaco-list-row.selected { outline: 1px dotted var(--vscode-contrastActiveBorder); outline-offset: -1px; }
.monaco-list.list_id_3 .monaco-list-row.focused { outline: 1px dotted var(--vscode-contrastActiveBorder); outline-offset: -1px; }
.monaco-list.list_id_3 .monaco-list-row:hover { outline: 1px dashed var(--vscode-contrastActiveBorder); outline-offset: -1px; }

				.monaco-list.list_id_3.drop-target,
				.monaco-list.list_id_3 .monaco-list-rows.drop-target,
				.monaco-list.list_id_3 .monaco-list-row.drop-target { background-color: var(--vscode-list-dropBackground) !important; color: inherit !important; }
			

				.monaco-table > .monaco-split-view2,
				.monaco-table > .monaco-split-view2 .monaco-sash.vertical::before,
				.monaco-workbench:not(.reduce-motion) .monaco-table:hover > .monaco-split-view2,
				.monaco-workbench:not(.reduce-motion) .monaco-table:hover > .monaco-split-view2 .monaco-sash.vertical::before {
					border-color: var(--vscode-tree-tableColumnsBorder);
				}

				.monaco-workbench:not(.reduce-motion) .monaco-table > .monaco-split-view2,
				.monaco-workbench:not(.reduce-motion) .monaco-table > .monaco-split-view2 .monaco-sash.vertical::before {
					border-color: transparent;
				}
			

				.monaco-table .monaco-list-row[data-parity=odd]:not(.focused):not(.selected):not(:hover) .monaco-table-tr,
				.monaco-table .monaco-list:not(:focus) .monaco-list-row[data-parity=odd].focused:not(.selected):not(:hover) .monaco-table-tr,
				.monaco-table .monaco-list:not(.focused) .monaco-list-row[data-parity=odd].focused:not(.selected):not(:hover) .monaco-table-tr {
					background-color: var(--vscode-tree-tableOddRowsBackground);
				}
			</style></div></div><div class="suggest-status-bar" style="height: 19px; display: none;" aria-hidden="true"><div class="monaco-action-bar animated left"><ul class="actions-container" role="presentation"><li class="action-item menu-entry" role="presentation" title="Insert (Enter)"><a class="action-label" role="button" aria-label="Insert (Enter)" aria-checked="" tabindex="0">Insert (⏎)</a></li></ul></div><div class="monaco-action-bar animated right"><ul class="actions-container" role="presentation"><li class="action-item menu-entry" role="presentation" title="show more (Ctrl+Space)"><a class="action-label" role="button" aria-label="show more (Ctrl+Space)" aria-checked="" tabindex="0">show more (Ctrl+Space)</a></li></ul></div></div></div><div class="editor-widget parameter-hints-widget" widgetid="editor.widget.parameterHintsWidget" style="user-select: text; position: fixed; display: none; visibility: hidden; max-width: 1366px; font-size: 14px; line-height: 1.35714; max-height: 250px; top: 273px; left: 246px;"><div class="phwrapper" tabindex="-1" style="max-height: 250px;"><div class="controls"><div class="button codicon codicon-parameter-hints-previous"></div><div class="overloads">1/1</div><div class="button codicon codicon-parameter-hints-next"></div></div><div class="monaco-scrollable-element " role="presentation" style="position: relative; overflow: hidden;"><div class="body" style="overflow: hidden;"><div class="signature has-docs"><div class="code" style="font-size: 14px; font-family: monospace;"><span>count</span></div></div><div class="docs"><p>int([x]) -&gt; integer
int(x, base=10) -&gt; integer

Convert a number or string to an integer, or return 0 if no arguments
are given.  If x is a number, return x.__int__().  For floating-point
numbers, this truncates towards zero.

If x is not a number or if base is given, then x must be a string,
bytes, or bytearray instance representing an integer literal in the
given base.  The literal can be preceded by '+' or '-' and be surrounded
by whitespace.  The base defaults to 10.  Valid bases are 0 and 2-36.
Base 0 means to interpret the base from the string as an integer literal.
&gt;&gt;&gt; int('0b100', base=0)
4</p></div></div><div role="presentation" aria-hidden="true" class="invisible scrollbar horizontal" style="position: absolute; width: 430px; height: 10px; left: 0px; bottom: 0px;"><div class="slider" style="position: absolute; top: 0px; left: 0px; height: 10px; transform: translate3d(0px, 0px, 0px); contain: strict; width: 430px;"></div></div><div role="presentation" aria-hidden="true" class="invisible scrollbar vertical fade" style="position: absolute; width: 10px; height: 250px; right: 0px; top: 0px;"><div class="slider" style="position: absolute; top: 0px; left: 0px; width: 10px; transform: translate3d(0px, 0px, 0px); contain: strict; height: 170px;"></div></div><div class="shadow"></div><div class="shadow"></div><div class="shadow"></div></div></div></div></div><div class=".in-cell-overflowing"><div widgetid="editor.contrib.quickInputWidget" style="position: absolute; top: 0px; right: 50%;"></div></div></div></div></div><colab-form class="formview vertical layout flex"><div class="widget-area vertical layout"></div></colab-form></div>
    <div class="output" aria-label="Cell 0 output" role="region"><!----> <div class="output-header"> </div>
        <div class="output-content">
          <div class="output-info"><colab-output-info></colab-output-info></div>
          <div class="output-iframe-container">
            <div class="output-iframe-sizer" style="min-height: 0px;"> <div><div><colab-static-output-renderer tabindex="0" role="group"><div><div class="stream output-id-2 output_text"><pre>welcome
how to make code
</pre></div></div><div></div></colab-static-output-renderer></div></div></div>
          </div>
        </div></div><colab-cell-next-steps></colab-cell-next-steps></div>