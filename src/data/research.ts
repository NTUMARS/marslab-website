// Research page curation — sections, sub-tracks, and representative works.
// Each item references a publication in src/content/publications/ by its id
// (without the locale prefix); title/venue/links/teaser are pulled from the
// collection at build time so nothing is duplicated here. `display` overrides
// the (often long) paper title with a card-sized name; `media` points to an
// animated teaser (usually under public/research/, but any site-absolute path
// works) — omit it to fall back to the publication's static image.

export interface ResearchItem {
	ref: string; // publications collection id, e.g. "action-to-action-flow-matching"
	display?: string; // card heading; defaults to the publication title
	blurb: string; // one editorial line under the heading
	badge?: "Dataset" | "Benchmark" | "New";
	media?: { video: string; poster: string }; // site-absolute paths, e.g. /research/foo.mp4
	fit?: "cover" | "contain"; // escape hatch for teasers that crop badly
}

export interface ResearchGroup {
	label?: string; // optional sub-track heading; no section splits into sub-tracks at present
	items: ResearchItem[];
}

export interface ResearchSection {
	id: string; // anchor slug
	num: string; // "01" — rendered in KaTeX_Main
	title: string;
	tagline: string; // one-line description, reused in the overview index
	groups: ResearchGroup[];
}

export const overviewLede = "Our research is organized into five interconnected directions:";

export const overviewClose =
	"Below are representative research projects, benchmark datasets, and open-source resources developed by our lab.";

export const sections: ResearchSection[] = [
	{
		id: "reliable-robot-learning",
		num: "01",
		title: "Reliable Robot Learning",
		tagline: "Robust and feedback-driven learning for precise, dependable manipulation.",
		groups: [
			{
				items: [
					{
						ref: "action-to-action-flow-matching",
						display: "A2A: Action-to-Action Flow Matching",
						blurb: "Flow matching directly from action to action for fast, precise, and robust visuomotor control.",
						badge: "New",
						media: {
							video: "/research/action-to-action-flow-matching.mp4",
							poster: "/research/action-to-action-flow-matching-poster.jpg",
						},
					},
					{
						ref: "feedback-world-model",
						display: "Feedback World Model",
						blurb: "A world model that self-corrects diffusion-policy guidance through real execution feedback.",
						media: {
							video: "/research/feedback-world-model.mp4",
							poster: "/research/feedback-world-model-poster.jpg",
						},
					},
				],
			},
		],
	},
	{
		id: "humanoid-loco-manipulation",
		num: "02",
		title: "Humanoid Whole-Body Loco-Manipulation",
		tagline: "Coordinating locomotion with manipulation, and holding steady under real-world disturbance.",
		groups: [
			{
				items: [
					{
						ref: "omega-0",
						display: "ω-0: Latent Predictive World Action Model",
						blurb: "Predicting the world in latent space so a humanoid can walk and manipulate as one concurrent policy.",
						// Reuses the publications teaser and hover clip rather than duplicating
						// 3 MB of near-identical media under /research/.
						media: {
							video: "/publications/zhe-omega0-arxiv26.mp4",
							poster: "/publications/zhe-omega0-arxiv26.png",
						},
					},
					{
						ref: "adapt",
						display: "ADAPT: Disturbance-Aware Policy Training",
						blurb: "Analytical disturbance-aware training keeps humanoid locomotion stable under pushes, pulls, and payloads.",
						media: {
							video: "/research/adapt.mp4",
							poster: "/research/adapt-poster.jpg",
						},
					},
				],
			},
		],
	},
	{
		id: "human-robot-interaction",
		num: "03",
		title: "Human-Robot Interaction",
		tagline: "Understanding human intention, attention, and communication for natural collaboration.",
		groups: [
			{
				items: [
					{
						ref: "gaze2act",
						display: "Gaze2Act: Gaze-Conditioned VLA Policies",
						blurb: "Reading human gaze to resolve what to pick, where to place, and how to act in ambiguous scenes.",
						media: {
							video: "/research/gaze2act.mp4",
							poster: "/research/gaze2act-poster.jpg",
						},
					},
					{
						ref: "abstain-eqa",
						display: 'AbstainEQA: When Robots Should Say "I Don\'t Know"',
						blurb: "Benchmarking abstention in embodied question answering — knowing when not to answer.",
						badge: "Benchmark",
					},
					{
						ref: "rei-bench",
						display: "REI-Bench: Vague Instructions in Task Planning",
						blurb: "Can embodied agents understand vague, human-style instructions when planning tasks?",
						badge: "Benchmark",
					},
				],
			},
		],
	},
	{
		id: "robot-perception",
		num: "04",
		title: "Robot Perception",
		tagline: "Exploring new sensors and multimodal perception model beyond vision.",
		groups: [
			{
				items: [
					{
						ref: "mm-fi",
						display: "MM-Fi: Multi-Modal 4D Human Sensing Dataset",
						blurb: "A non-intrusive 4D human dataset spanning WiFi, mmWave radar, LiDAR, and RGB-D modalities.",
						badge: "Dataset",
					},
					{
						ref: "compassad",
						display: "CompassAD: Intent-Driven 3D Affordance Grounding",
						blurb: "Grounding 3D affordances by intent among functionally competing objects in cluttered scenes.",
					},
					{
						ref: "activevital",
						display: "ActiveVital: Geometry-Aware Vital Signs Monitoring",
						blurb: "Treating radar pose as a controllable variable — the robot moves to face the chest and reads respiration and heartbeat cleanly.",
						// Teaser is a 2.36:1 multi-panel figure; cover would clip the outer panels.
						fit: "contain",
					},
				],
			},
		],
	},
	{
		id: "physical-agents",
		num: "05",
		title: "Physical Agents",
		tagline: "AI agents that bridge digital intelligence with physical environments, devices, and robots.",
		groups: [
			{
				items: [
					{
						ref: "iot-llm",
						display: "IoT-LLM: LLM Reasoning over Real-World Sensors",
						blurb: "Enhancing large language model reasoning with real-world IoT sensor data for physical-world tasks.",
					},
				],
			},
		],
	},
];
