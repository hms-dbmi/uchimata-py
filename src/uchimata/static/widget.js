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
      center: false,
      normalize: false,
    };

    //~ create a scene
    let chromatinScene = uchi.initScene();

    const structures = model.get("structures");
    const viewconfigs = model.get("viewconfigs");

    //~ displayable structure = structure + viewconfig
    const displayableStructures = [];
    for (const [i, s] of structures.entries()) {
      displayableStructures.push({ structure: s, viewConfig: viewconfigs[i] });
    }

    if (
      displayableStructures.length === 0 ||
      displayableStructures[0].structure === undefined
    ) {
      console.error("suplied structure is UNDEFINED");
    }

    /** @type {import("http://localhost:5173/src/main.ts").ViewConfig} */
    const defaultViewConfig = {
      color: "red",
      scale: 0.01,
    };

    for (const ds of displayableStructures) {
      console.log("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~");
      const vc = (ds.viewConfig === undefined)
        ? defaultViewConfig
        : ds.viewConfig;
      const structure = uchi.load(ds.structure.buffer, options);
      chromatinScene = uchi.addStructureToScene(
        chromatinScene,
        structure,
        vc,
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
