// @deno-types="npm:uchimata"
import * as uchi from "https://esm.sh/uchimata@^0.3.x";

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
    let chromatinScene = uchi.initScene();

    //~ process input
    /** @type {DataView} */
    const structure = model.get("structure");
    const viewConfig = model.get("viewconfig");
    if (structure === undefined) {
      console.error("suplied structure is UNDEFINED");
    }
    console.log(viewConfig);
    const chunkOrModel = uchi.load(structure.buffer, options); //~ TODO: better name for this variable

    //const isModel = "parts" in chunkOrModel; //~ ChromatinModel has .parts

    /** @type {import("http://localhost:5173/src/main.ts").ViewConfig} */
    const defaultViewConfig = {
      scale: 0.01,
    };

    //if (isModel) {
    //  defaultViewConfig = {
    //    scale: 0.008,
    //  };
    //} else {
    //  //~ this config specifies how the 3D model will look
    //  const binsNum = chunkOrModel.bins.length;
    //  const sequenceValues = Array.from({ length: binsNum }, (_, i) => i);
    //  defaultViewConfig = {
    //    scale: 0.01,
    //    color: {
    //      values: sequenceValues,
    //      min: 0,
    //      max: binsNum - 1,
    //      colorScale: "viridis",
    //    },
    //    links: true,
    //  };
    //}

    const viewConfigNotSupplied = viewConfig === undefined ||
      Object.keys(viewConfig).length === 0;
    const vc = viewConfigNotSupplied ? defaultViewConfig : viewConfig;

    chromatinScene = uchi.addStructureToScene(
      chromatinScene,
      chunkOrModel,
      vc,
    );

    const [renderer, canvas] = uchi.display(chromatinScene, {
      alwaysRedraw: false,
    });
    el.appendChild(canvas);

    return () => {
      // Optionally cleanup
      renderer.endDrawing();
    };
  },
};
