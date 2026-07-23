import { IGlobeEngine, ICameraManager, ILayerManager } from '../core/IGlobeEngine';
import { engineEvents, EngineEvent } from '../events/EventBus';
import { createRoot, Root } from 'react-dom/client';
import React from 'react';
import { Globe3D } from '@/components/Globe3D';

// Mock Managers for Three.js (until fully implemented)
class ThreeJsCameraManager implements ICameraManager {
  flyTo(lat: number, lng: number, altitude?: number): void {
    console.log(`[ThreeJsEngine] Flying to ${lat}, ${lng} at ${altitude}`);
  }
  pan(dx: number, dy: number): void {}
  zoom(level: number): void {}
}

class ThreeJsLayerManager implements ILayerManager {
  addLayer(id: string, config: any): void {}
  removeLayer(id: string): void {}
  toggleLayer(id: string, visible: boolean): void {}
}

export class ThreeJsEnginePlugin implements IGlobeEngine {
  engineName = 'threejs';
  private reactRoot: Root | null = null;
  private cameraManager = new ThreeJsCameraManager();
  private layerManager = new ThreeJsLayerManager();

  initialize(container: HTMLElement): void {
    console.log('[ThreeJsEngine] Initializing...');
    
    // We mount the existing React-based Globe3D component 
    // into the raw HTML element provided by the wrapper.
    this.reactRoot = createRoot(container);
    this.reactRoot.render(
      React.createElement(Globe3D)
    );

    // Listen to global events
    engineEvents.on(EngineEvent.CAMERA_FLY_TO, this.handleFlyTo.bind(this));
  }

  private handleFlyTo(payload: any) {
    this.cameraManager.flyTo(payload.lat, payload.lng, payload.alt);
  }

  destroy(): void {
    console.log('[ThreeJsEngine] Destroying...');
    engineEvents.off(EngineEvent.CAMERA_FLY_TO, this.handleFlyTo.bind(this));
    
    if (this.reactRoot) {
      this.reactRoot.unmount();
      this.reactRoot = null;
    }
  }

  resize(): void {
    // Handled natively by react-three-fiber's Canvas
  }

  getCameraManager(): ICameraManager {
    return this.cameraManager;
  }

  getLayerManager(): ILayerManager {
    return this.layerManager;
  }
}
