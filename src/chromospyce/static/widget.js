// @deno-types="npm:chromospace"
// import * as chs from "https://esm.sh/chromospace@^0.1.x";
import * as chs from "http://localhost:5173/src/main.ts";

/**
 * @typedef TextFile
 * @property {string} name
 * @property {string} contents
 */

/**
 * @typedef Model
 * @property {DataView} [nparr_model]
 * @property {boolean} is_numpy
 * @property {TextFile} model
 * @property {string} delimiter
 */

export default {
  /** @type {import("npm:@anywidget/types@0.1.6").Render<Model>} */
  render({ model, el }) {
    const options = {
      center: true,
      normalize: true,
    };

    //~ create a scene
    let chromatinScene = chs.initScene();

    //~ process input
    /** @type {DataView} */
    const structure = model.get("structure");
    const viewConfig = model.get("viewconfig");
    if (structure === undefined) {
      console.error("suplied structure is UNDEFINED");
    }
    console.log(viewConfig);
    const chunk = chs.load(structure.buffer, options);

    //~ this config specifies how the 3D model will look
    const binsNum = chunk.bins.length;
    const sequenceValues = Array.from({ length: binsNum }, (_, i) => i);
    const defaultViewConfig = {
      scale: 0.01,
      color: {
        values: sequenceValues,
        min: 0,
        max: binsNum - 1,
        colorScale: "viridis",
      },
      links: true,
    };

    const viewConfigNotSupplied = viewConfig === undefined ||
      Object.keys(viewConfig).length === 0;
    const vc = viewConfigNotSupplied ? defaultViewConfig : viewConfig;

    if (isModel) {
      chromatinScene = chs.addModelToScene(chromatinScene, chunk, vc);
    } else {
      chromatinScene = chs.addChunkToScene(chromatinScene, chunk, vc);
    }

    const [renderer, canvas] = chs.display(chromatinScene, {
      alwaysRedraw: false,
    });
    el.appendChild(canvas);

    return () => {
      // Optionally cleanup
      renderer.endDrawing();
    };
  },
};
