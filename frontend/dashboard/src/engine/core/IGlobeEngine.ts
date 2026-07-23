// Core interfaces for the Enterprise Rendering Platform

export interface ICameraManager {
  flyTo(lat: number, lng: number, altitude?: number): void;
  pan(dx: number, dy: number): void;
  zoom(level: number): void;
}

export interface ILayerManager {
  addLayer(id: string, config: any): void;
  removeLayer(id: string): void;
  toggleLayer(id: string, visible: boolean): void;
}

export interface IGlobeEngine {
  engineName: string;
  
  // Lifecycle
  initialize(container: HTMLElement): void;
  destroy(): void;
  resize(): void;
  
  // Managers
  getCameraManager(): ICameraManager;
  getLayerManager(): ILayerManager;
}
