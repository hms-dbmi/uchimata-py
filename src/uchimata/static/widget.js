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

    //~ displayable structure = structure + viewconfig
    const displayableStructures = [{
      structure: structure,
      viewConfig: viewConfig,
    }];

    if (
      displayableStructures.length === 0 ||
      displayableStructures[0].structure === undefined
    ) {
      console.error("suplied structure is UNDEFINED");
    }
    console.log(viewConfig);
    // const chunkOrModel = uchi.load(structure.buffer, options); //~ TODO: better name for this variable

    /** @type {import("http://localhost:5173/src/main.ts").ViewConfig} */
    const defaultViewConfig = {
      scale: 0.01,
    };

    const viewConfigNotSupplied = viewConfig === undefined ||
      Object.keys(viewConfig).length === 0;
    const vc = viewConfigNotSupplied ? defaultViewConfig : viewConfig;

    for (const ds of displayableStructures) {
      console.log("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~");
      chromatinScene = uchi.addStructureToScene(
        chromatinScene,
        uchi.load(ds.structure.buffer, options),
        ds.viewConfig,
      );
    }

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
