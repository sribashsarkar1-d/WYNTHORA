import { useRef, useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Sphere, Line, Stars, OrbitControls, Html } from '@react-three/drei';
import * as THREE from 'three';

// Helper to convert lat/lng to 3D Cartesian coordinates
function getPosFromLatLng(lat: number, lng: number, radius: number): [number, number, number] {
  const phi = (90 - lat) * (Math.PI / 180);
  const theta = (lng + 180) * (Math.PI / 180);
  return [
    -(radius * Math.sin(phi) * Math.cos(theta)),
    radius * Math.cos(phi),
    radius * Math.sin(phi) * Math.sin(theta)
  ];
}

// Data points for the globe
const markers = [
  { name: "New York", lat: 40.71, lng: -74.00, type: "economy" },
  { name: "London", lat: 51.50, lng: -0.12, type: "economy" },
  { name: "Tokyo", lat: 35.67, lng: 139.65, type: "economy" },
  { name: "Dubai", lat: 25.20, lng: 55.27, type: "trade" },
  { name: "Singapore", lat: 1.35, lng: 103.81, type: "trade" },
  { name: "Frankfurt", lat: 50.11, lng: 8.68, type: "economy" },
  { name: "Conflict Zone A", lat: 48.37, lng: 31.16, type: "risk" },
];

function Earth() {
  const earthRef = useRef<THREE.Group>(null);
  const R = 2; // Radius

  // Stylized materials
  const coreMaterial = useMemo(() => new THREE.MeshPhongMaterial({
    color: '#080d14',
    emissive: '#041024',
    emissiveIntensity: 0.5,
    shininess: 50,
  }), []);

  const gridMaterial = useMemo(() => new THREE.MeshBasicMaterial({
    color: '#1a4b8c',
    wireframe: true,
    transparent: true,
    opacity: 0.15
  }), []);

  const atmosphereMaterial = useMemo(() => new THREE.MeshBasicMaterial({
    color: '#4db8ff',
    transparent: true,
    opacity: 0.08,
    side: THREE.BackSide,
    blending: THREE.AdditiveBlending
  }), []);

  useFrame((state) => {
    if (earthRef.current) {
      earthRef.current.rotation.y = state.clock.getElapsedTime() * 0.05;
    }
  });

  return (
    <group ref={earthRef}>
      {/* Solid Core */}
      <Sphere args={[R, 64, 64]}>
        <primitive object={coreMaterial} attach="material" />
      </Sphere>
      
      {/* Wireframe overlay */}
      <Sphere args={[R + 0.01, 32, 32]}>
        <primitive object={gridMaterial} attach="material" />
      </Sphere>
      
      {/* Atmosphere Glow */}
      <Sphere args={[R + 0.3, 32, 32]}>
        <primitive object={atmosphereMaterial} attach="material" />
      </Sphere>

      {/* Interactive Markers */}
      {markers.map((marker, i) => {
        const pos = getPosFromLatLng(marker.lat, marker.lng, R);
        const isRisk = marker.type === "risk";
        const color = isRisk ? "#ff3366" : (marker.type === "trade" ? "#a371f7" : "#4db8ff");
        
        return (
          <group key={i} position={pos}>
            <mesh>
              <sphereGeometry args={[0.03, 16, 16]} />
              <meshBasicMaterial color={color} />
            </mesh>
            {/* Pulsing ring */}
            <mesh>
              <ringGeometry args={[0.04, 0.06, 32]} />
              <meshBasicMaterial color={color} transparent opacity={0.5} side={THREE.DoubleSide} />
            </mesh>
            {/* HTML Label */}
            <Html distanceFactor={15} center>
              <div className="pointer-events-none flex flex-col items-center">
                <div className={`px-2 py-0.5 rounded text-[10px] font-bold text-white whitespace-nowrap bg-black/50 backdrop-blur-sm border ${isRisk ? 'border-red-500/50' : 'border-cyan/50'}`}>
                  {marker.name}
                </div>
              </div>
            </Html>
          </group>
        );
      })}

      {/* Decorative Data Arcs (Connections) */}
      <Line points={[getPosFromLatLng(40.71, -74.00, R), getPosFromLatLng(51.50, -0.12, R)]} color="#4db8ff" lineWidth={1.5} transparent opacity={0.6} />
      <Line points={[getPosFromLatLng(51.50, -0.12, R), getPosFromLatLng(25.20, 55.27, R)]} color="#a371f7" lineWidth={1.5} transparent opacity={0.6} />
      <Line points={[getPosFromLatLng(25.20, 55.27, R), getPosFromLatLng(1.35, 103.81, R)]} color="#a371f7" lineWidth={1.5} transparent opacity={0.6} />
      <Line points={[getPosFromLatLng(1.35, 103.81, R), getPosFromLatLng(35.67, 139.65, R)]} color="#4db8ff" lineWidth={1.5} transparent opacity={0.6} />
      
    </group>
  );
}

export function Globe3D() {
  return (
    <div className="w-full h-full min-h-[400px] cursor-move flex-1 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-[#0d1522] via-[#080c14] to-[#04060a]">
      <Canvas camera={{ position: [0, 0, 5.5], fov: 45 }} gl={{ antialias: true, alpha: true }}>
        <ambientLight intensity={0.8} color="#4db8ff" />
        <pointLight position={[10, 10, 10]} intensity={2} color="#ffffff" />
        <pointLight position={[-10, -10, -10]} intensity={0.5} color="#a371f7" />
        <Stars radius={100} depth={50} count={3000} factor={4} saturation={1} fade speed={1.5} />
        <Earth />
        <OrbitControls 
          enableZoom={true} 
          enablePan={false}
          enableDamping={true}
          dampingFactor={0.05}
          minDistance={3}
          maxDistance={10}
        />
      </Canvas>
    </div>
  );
}
