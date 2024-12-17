// @deno-types="npm:chromospace"
import * as chs from "https://esm.sh/chromospace@^0.1.x";

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
		const query = model.get("selection_query");
		if (structure === undefined) {
			console.error("suplied structure is UNDEFINED");
		}
		console.log(viewConfig);
		const chunkOrModel = chs.load(structure.buffer, options);

		// const isModel = true;
		const isModel = "parts" in chunkOrModel; //~ ChromatinModel has .parts

		/** @type {import("http://localhost:5173/src/main.ts").ViewConfig} */
		let defaultViewConfig = {
			scale: 0.01,
		};

		if (isModel) {
			defaultViewConfig = {
				scale: 0.008,
			};
		} else {
			//~ this config specifies how the 3D model will look
			const binsNum = chunkOrModel.bins.length;
			const sequenceValues = Array.from({ length: binsNum }, (_, i) => i);
			defaultViewConfig = {
				scale: 0.01,
				color: {
					values: sequenceValues,
					min: 0,
					max: binsNum - 1,
					colorScale: "viridis",
				},
				links: true,
			};
		}

		const viewConfigNotSupplied =
			viewConfig === undefined || Object.keys(viewConfig).length === 0;
		const vc = viewConfigNotSupplied ? defaultViewConfig : viewConfig;

		if (isModel) {
			console.log("model from anywidget");
			const model = chunkOrModel;
			if (query !== "") {
				const [part, _] = chs.get(model, query);
				const newModel = {
					parts: [part],
				};
				chromatinScene = chs.addModelToScene(chromatinScene, newModel, vc);
			} else {
				chromatinScene = chs.addModelToScene(chromatinScene, model, vc);
			}
		} else {
			console.log("chunk from anywidget");
			const chunk = chunkOrModel;
			chromatinScene = chs.addChunkToScene(chromatinScene, chunk, vc);
		}

		const [renderer, canvas] = chs.display(chromatinScene, {
			alwaysRedraw: false,
		});
		el.appendChild(canvas);
		console.log("~~~~~~~~ HI ~~~~~~~~~~");

		// function onQueryChange() {
		// 	const query = model.get("selection_query");
		// 	console.log(`The 'selection_query' changed to: ${query}`);
		// 	if (isModel) {
		// 		const chModel = chunkOrModel;
		// 		const [selectedPart, _] = chs.get(chModel, query);
		// 		const selectedModel = {
		// 			parts: [selectedPart],
		// 		};
		// 		const newScene = chs.initScene();
		// 		chs.addModelToScene(newScene, selectedModel, {
		// 			color: "red",
		// 			binSizeScale: 0.1,
		// 		});
		// 		console.log(
		// 			`selectedPart # of bins: ${selectedPart.chunk.bins.length}`,
		// 		);
		//
		// 		const [renderer, canvas] = chs.display(newScene, {
		// 			alwaysRedraw: false,
		// 		});
		// 		el.replaceChildren();
		// 		el.appendChild(canvas);
		// 	} else {
		// 		console.log("chs.get() called on a ChromatinChunk");
		// 	}
		// }
		// model.on("change:selection_query", onQueryChange);

		return () => {
			// Optionally cleanup
			renderer.endDrawing();
		};
	},
};
