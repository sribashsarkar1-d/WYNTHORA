type EventHandler<T = any> = (payload: T) => void;

export class EventBus {
  private static instance: EventBus;
  private listeners: Map<string, EventHandler[]> = new Map();

  private constructor() {}

  public static getInstance(): EventBus {
    if (!EventBus.instance) {
      EventBus.instance = new EventBus();
    }
    return EventBus.instance;
  }

  public on<T = any>(event: string, handler: EventHandler<T>): void {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event)!.push(handler);
  }

  public off<T = any>(event: string, handler: EventHandler<T>): void {
    if (!this.listeners.has(event)) return;
    
    const handlers = this.listeners.get(event)!;
    const index = handlers.indexOf(handler);
    if (index !== -1) {
      handlers.splice(index, 1);
    }
    
    if (handlers.length === 0) {
      this.listeners.delete(event);
    }
  }

  public emit<T = any>(event: string, payload?: T): void {
    if (!this.listeners.has(event)) return;
    
    const handlers = this.listeners.get(event)!;
    // Call all handlers synchronously
    for (const handler of handlers) {
      try {
        handler(payload);
      } catch (error) {
        console.error(`Error executing event handler for ${event}:`, error);
      }
    }
  }
}

// Global convenience export
export const engineEvents = EventBus.getInstance();

// Typed event names
export enum EngineEvent {
  CAMERA_FLY_TO = 'CAMERA_FLY_TO',
  LAYER_TOGGLE = 'LAYER_TOGGLE',
  ENTITY_SELECT = 'ENTITY_SELECT',
  TIME_UPDATE = 'TIME_UPDATE',
  THEME_CHANGE = 'THEME_CHANGE'
}
