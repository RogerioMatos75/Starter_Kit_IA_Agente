"use client";

const paths = [
  // Top connections
  "M 400 215 L 400 25",
  "M 380 215 L 380 50 L 150 50",
  "M 420 215 L 420 50 L 650 50",
  "M 360 215 L 360 100 L 100 100",
  "M 440 215 L 440 100 L 700 100",

  // Bottom connections
  "M 400 385 L 400 575",
  "M 380 385 L 380 550 L 150 550",
  "M 420 385 L 420 550 L 650 550",
  "M 360 385 L 360 500 L 100 500",
  "M 440 385 L 440 500 L 700 500",

  // Left connections
  "M 340 300 L 25 300",
  "M 340 250 L 50 250",
  "M 340 350 L 50 350",
  "M 340 280 L 150 280 L 150 150",
  "M 340 320 L 150 320 L 150 450",

  // Right connections
  "M 460 300 L 775 300",
  "M 460 250 L 750 250",
  "M 460 350 L 750 350",
  "M 460 280 L 650 280 L 650 150",
  "M 460 320 L 650 320 L 650 450",

  // Field lines (grid)
  "M 200 50 L 200 550", // Vertical
  "M 600 50 L 600 550", // Vertical
  "M 50 120 L 750 120", // Horizontal
  "M 50 480 L 750 480", // Horizontal
  "M 275 50 L 275 550", // Vertical
  "M 525 50 L 525 550", // Vertical
  "M 50 200 L 750 200", // Horizontal
  "M 50 400 L 750 400", // Horizontal
];

const endPoints = paths.map(path => {
  const coords = path.match(/(\d+)\s(\d+)$/);
  if (coords) {
    return { cx: parseInt(coords[1], 10), cy: parseInt(coords[2], 10) };
  }
  // This fallback should ideally not be reached with the current path data.
  return { cx: 0, cy: 0 };
});

const numPulsesPerPath = 3;

export function ChipAnimation() {
  return (
    <div className="w-full h-full flex items-center justify-center overflow-hidden relative" data-ai-hint="chip circuit">
      <style jsx global>{`
        .pulse {
          position: absolute;
          top: 0;
          left: 0;
          width: 8px;
          height: 8px;
          border-radius: 50%;
          background: var(--pulse-color, #FFD700);
          box-shadow: 0 0 var(--intensity, 8px) var(--pulse-color, #FFD700), 0 0 calc(var(--intensity, 8px) * 1.5) var(--pulse-color, #FFD700);
          animation-name: followPath;
          animation-duration: var(--speed, 5s);
          animation-timing-function: linear;
          animation-iteration-count: infinite;
          offset-path: var(--path);
          offset-distance: 0%;
          offset-rotate: 0deg;
          will-change: offset-distance;
        }

        @keyframes followPath {
          from {
            offset-distance: 0%;
          }
          to {
            offset-distance: 100%;
          }
        }
      `}</style>

      <svg
        viewBox="0 0 800 600"
        className="w-full h-full"
        preserveAspectRatio="xMidYMid meet"
      >
        <defs>
          {paths.map((d, i) => (
            <path id={`path-${i}`} key={i} d={d} />
          ))}
        </defs>

        <g stroke="var(--bus-color, #a0a0a0)" strokeWidth="0.5" fill="none" strokeLinecap="round">
          {paths.map((_, i) => (
            <use key={i} href={`#path-${i}`} />
          ))}
        </g>

        <g fill="var(--bus-color, #a0a0a0)">
          {endPoints.map((point, i) => (
            <circle key={`end-${i}`} cx={point.cx} cy={point.cy} r="5" />
          ))}
        </g>

        <rect
          x="340"
          y="215"
          width="120"
          height="170"
          fill="hsl(var(--secondary))"
          stroke="var(--bus-color, #a0a0a0)"
          strokeWidth="2"
          rx="8"
        />
        <rect
          x="350"
          y="225"
          width="100"
          height="150"
          fill="hsl(var(--background))"
          stroke="var(--bus-color, #a0a0a0)"
          strokeWidth="4"
          rx="5"
        />
        <text
          x="400"
          y="305"
          textAnchor="middle"
          fill="var(--bus-color, #a0a0a0)"
          fontSize="24"
          fontWeight="bold"
          className="font-headline"
        >
          Archon
        </text>
      </svg>

      <div className="absolute top-0 left-0 w-full h-full pointer-events-none">
        {paths.map((path, pathIndex) =>
          Array.from({ length: numPulsesPerPath }).map((_, pulseIndex) => {
            return (
              <div
                key={`${pathIndex}-${pulseIndex}`}
                className="pulse"
                style={{
                  // @ts-ignore
                  '--path': `url(#path-${pathIndex})`,
                  animationDelay: `-${(pulseIndex * 1.5 + pathIndex * 0.3).toFixed(2)}s`,
                }}
              />
            )
          })
        )}
      </div>
    </div>
  );
}
