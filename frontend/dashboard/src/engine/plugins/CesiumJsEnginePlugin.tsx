import { IGlobeEngine, ICameraManager, ILayerManager } from '../core/IGlobeEngine';
import { engineEvents, EngineEvent } from '../events/EventBus';
import { createRoot, Root } from 'react-dom/client';
import React, { useRef, useEffect, useState } from 'react';
import { Viewer, Scene, Globe, Fog, SkyAtmosphere, Cesium3DTileset, Entity, PolygonGraphics, PointGraphics, ImageryLayer } from 'resium';
import * as Cesium from 'cesium';

// Import mandatory Cesium CSS for proper rendering and sizing
import 'cesium/Build/Cesium/Widgets/widgets.css';

// Set default Ion Token
Cesium.Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI4YTNkNjQxYS0zYTBhLTRlMTQtYjAyOC0yMDU2NzY3NDYzOTYiLCJpZCI6NDU0ODk2LCJzdWIiOiJzMjBiIiwiaXNzIjoiaHR0cHM6Ly9hcGkuY2VzaXVtLmNvbSIsImF1ZCI6Ild5bnRob3JhIiwiaWF0IjoxNzgzNjg2NDEwfQ.n77-Hlts8PzIpLpGC27tZpmK38GfHTucOECefTkneIk';

// --- Phase 3: Mock Data Component ---
const MockSimulationLayer = ({ activeLayers }: { activeLayers: Set<string> }) => {
  // Mock War Zone (Ukraine region)
  const warZoneHierarchy = Cesium.Cartesian3.fromDegreesArray([
    24.0, 48.0, 
    38.0, 48.0, 
    38.0, 52.0, 
    24.0, 52.0
  ]);

  // Mock Flight position using a CallbackProperty for animation
  const flightPos = new Cesium.CallbackProperty((time?: Cesium.JulianDate) => {
    if (!time) return Cesium.Cartesian3.ZERO;
    const seconds = Cesium.JulianDate.secondsDifference(time, Cesium.JulianDate.now());
    const lat = 51.5 + Math.sin(seconds * 0.5) * 5;
    const lng = -0.1 + Math.cos(seconds * 0.5) * 5;
    return Cesium.Cartesian3.fromDegrees(lng, lat, 100000);
  }, false);

  const showConflict = activeLayers.has("Conflict zones");
  const showFlight = activeLayers.has("Trade routes");
  const showEcon = activeLayers.has("Economic indicators");

  return (
    <>
      {showConflict && (
        <Entity name="Conflict Zone Alpha" description="High risk area">
          <PolygonGraphics 
            hierarchy={new Cesium.PolygonHierarchy(warZoneHierarchy)}
            material={Cesium.Color.RED.withAlpha(0.4)}
            extrudedHeight={5000}
          />
        </Entity>
      )}

      {showFlight && (
        <Entity name="Flight WYN-101" position={flightPos as any}>
          <PointGraphics pixelSize={10} color={Cesium.Color.YELLOW} outlineColor={Cesium.Color.WHITE} outlineWidth={2} />
        </Entity>
      )}
      
      {showEcon && (
        <Entity name="Economic Hub" position={Cesium.Cartesian3.fromDegrees(10.45, 51.16, 0)}>
          <PointGraphics pixelSize={25} color={Cesium.Color.GREEN.withAlpha(0.6)} />
        </Entity>
      )}
    </>
  );
};

interface CesiumAppProps {
  onViewerReady: (viewer: Cesium.Viewer) => void;
}

const CesiumApp: React.FC<CesiumAppProps> = ({ onViewerReady }) => {
  const viewerRef = useRef<any>(null);
  const [buildingAsset, setBuildingAsset] = useState<Cesium.IonResource | null>(null);
  const [imageryProvider, setImageryProvider] = useState<Cesium.ImageryProvider | null>(null);
  
  // Default layers that are checked in app.world.tsx
  const [activeLayers, setActiveLayers] = useState<Set<string>>(
    new Set(["Economic indicators", "Climate models", "Trade routes"])
  );

  useEffect(() => {
    if (viewerRef.current?.cesiumElement) {
      onViewerReady(viewerRef.current.cesiumElement);
    }
    
    // Load Bing Maps Hybrid (Aerial with Labels and Roads)
    Cesium.IonImageryProvider.fromAssetId(3)
      .then(provider => setImageryProvider(provider))
      .catch(err => console.error("Failed to load Hybrid Imagery", err));

    // Load OSM Buildings (which sit on top of the globe, allowing labels to show)
    Cesium.IonResource.fromAssetId(96188)
      .then(setBuildingAsset)
      .catch(err => console.error("Failed to load OSM Buildings", err));

    // Listen to sidebar UI toggles
    const handleLayerToggle = (payload: any) => {
      setActiveLayers(prev => {
        const next = new Set(prev);
        if (payload.visible) next.add(payload.id);
        else next.delete(payload.id);
        return next;
      });
    };
    engineEvents.on(EngineEvent.LAYER_TOGGLE, handleLayerToggle);

    return () => {
      engineEvents.off(EngineEvent.LAYER_TOGGLE, handleLayerToggle);
    };
  }, [onViewerReady]);

  return (
    <div style={{ width: '100%', height: '100%', position: 'absolute', top: 0, left: 0 }}>
      <Viewer 
        ref={viewerRef}
        timeline={true} 
        animation={true} 
        baseLayerPicker={false}
        geocoder={false}
        homeButton={false}
        infoBox={true}
        navigationHelpButton={false}
        sceneModePicker={false}
        fullscreenButton={false}
        style={{ width: '100%', height: '100%' }}
      >
        <Scene
          requestRenderMode={false}
          highDynamicRange={true}
        >
          <Globe 
            enableLighting={true} 
            showWaterEffect={true} 
            depthTestAgainstTerrain={true} 
          />
          <SkyAtmosphere />
          <Fog enabled={true} />
        </Scene>

        {/* Labels and Street Names */}
        {imageryProvider && <ImageryLayer imageryProvider={imageryProvider} />}

        {/* Phase 3/4: 3D OSM Buildings or Google Photorealistic Tiles */}
        {buildingAsset && <Cesium3DTileset url={buildingAsset as any} />}

        {/* Phase 3: Simulation Layers */}
        <MockSimulationLayer activeLayers={activeLayers} />

      </Viewer>
    </div>
  );
};

// Mock Managers for CesiumJS
class CesiumCameraManager implements ICameraManager {
  private viewer: Cesium.Viewer | null = null;

  setViewer(viewer: Cesium.Viewer) {
    this.viewer = viewer;
  }

  flyTo(lat: number, lng: number, altitude: number = 3000000): void {
    if (!this.viewer) return;
    
    this.viewer.camera.flyTo({
      destination: Cesium.Cartesian3.fromDegrees(lng, lat, altitude),
      duration: 2.0,
      easingFunction: Cesium.EasingFunction.QUADRATIC_IN_OUT
    });
  }
  
  pan(dx: number, dy: number): void {}
  zoom(level: number): void {}
}

class CesiumLayerManager implements ILayerManager {
  addLayer(id: string, config: any): void {}
  removeLayer(id: string): void {}
  toggleLayer(id: string, visible: boolean): void {}
}

export class CesiumJsEnginePlugin implements IGlobeEngine {
  engineName = 'cesiumjs';
  private reactRoot: Root | null = null;
  private cameraManager = new CesiumCameraManager();
  private layerManager = new CesiumLayerManager();

  initialize(container: HTMLElement): void {
    console.log('[CesiumEngine] Initializing with Ion Token...');
    
    this.reactRoot = createRoot(container);
    this.reactRoot.render(
      <CesiumApp onViewerReady={(viewer) => this.cameraManager.setViewer(viewer)} />
    );

    engineEvents.on(EngineEvent.CAMERA_FLY_TO, this.handleFlyTo.bind(this));
  }

  private handleFlyTo(payload: any) {
    this.cameraManager.flyTo(payload.lat, payload.lng, payload.alt);
  }

  destroy(): void {
    console.log('[CesiumEngine] Destroying...');
    engineEvents.off(EngineEvent.CAMERA_FLY_TO, this.handleFlyTo.bind(this));
    
    if (this.reactRoot) {
      this.reactRoot.unmount();
      this.reactRoot = null;
    }
  }

  resize(): void {
    // Handled natively by Resium/Cesium Viewer
  }

  getCameraManager(): ICameraManager {
    return this.cameraManager;
  }

  getLayerManager(): ILayerManager {
    return this.layerManager;
  }
}
