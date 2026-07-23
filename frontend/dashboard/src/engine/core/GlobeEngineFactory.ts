import { IGlobeEngine } from './IGlobeEngine';

export class GlobeEngineFactory {
  // We keep references to async loaded modules to avoid heavy bundling
  // if an engine is never used.

  static async createEngine(type: 'cesiumjs' | 'threejs'): Promise<IGlobeEngine> {
    if (type === 'cesiumjs') {
      // Lazy load Cesium plugin
      const { CesiumJsEnginePlugin } = await import('../plugins/CesiumJsEnginePlugin');
      return new CesiumJsEnginePlugin();
    } else if (type === 'threejs') {
      // Lazy load ThreeJS plugin
      const { ThreeJsEnginePlugin } = await import('../plugins/ThreeJsEnginePlugin');
      return new ThreeJsEnginePlugin();
    }
    
    throw new Error(`Unknown engine type: ${type}`);
  }
}
