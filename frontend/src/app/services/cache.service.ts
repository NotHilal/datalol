import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { tap } from 'rxjs/operators';

/**
 * Cache entry with data and expiration timestamp
 */
interface CacheEntry<T> {
  data: T;
  timestamp: number;
  ttl: number;  // Time to live in milliseconds
}

/**
 * Service-level caching for API responses
 * Implements LRU (Least Recently Used) eviction policy
 */
@Injectable({
  providedIn: 'root'
})
export class CacheService {
  private cache = new Map<string, CacheEntry<any>>();
  private accessOrder: string[] = [];  // For LRU tracking
  private readonly maxSize = 100;  // Maximum cache entries

  constructor() {
    // Clear expired entries every 60 seconds
    setInterval(() => this.clearExpired(), 60000);
  }

  /**
   * Get cached data if available and not expired
   */
  get<T>(key: string): T | null {
    const entry = this.cache.get(key);

    if (!entry) {
      return null;
    }

    // Check if expired
    const now = Date.now();
    if (now - entry.timestamp > entry.ttl) {
      this.cache.delete(key);
      this.removeFromAccessOrder(key);
      return null;
    }

    // Update LRU access order
    this.updateAccessOrder(key);

    return entry.data as T;
  }

  /**
   * Set data in cache with TTL (time to live in milliseconds)
   */
  set<T>(key: string, data: T, ttl: number = 300000): void {  // Default 5 minutes
    // Enforce max size (LRU eviction)
    if (this.cache.size >= this.maxSize && !this.cache.has(key)) {
      this.evictLRU();
    }

    this.cache.set(key, {
      data,
      timestamp: Date.now(),
      ttl
    });

    this.updateAccessOrder(key);
  }

  /**
   * Wrap an Observable with caching
   * Returns cached data if available, otherwise executes observable and caches result
   */
  wrap<T>(key: string, observable: Observable<T>, ttl: number = 300000): Observable<T> {
    const cached = this.get<T>(key);

    if (cached !== null) {
      console.log(`[Cache HIT] ${key}`);
      return of(cached);
    }

    console.log(`[Cache MISS] ${key}`);
    return observable.pipe(
      tap(data => this.set(key, data, ttl))
    );
  }

  /**
   * Invalidate (remove) specific cache entry
   */
  invalidate(key: string): void {
    this.cache.delete(key);
    this.removeFromAccessOrder(key);
  }

  /**
   * Invalidate all cache entries matching a pattern
   * Example: invalidatePattern('matches:') clears all match-related cache
   */
  invalidatePattern(pattern: string): void {
    const keysToDelete: string[] = [];

    this.cache.forEach((_, key) => {
      if (key.includes(pattern)) {
        keysToDelete.push(key);
      }
    });

    keysToDelete.forEach(key => this.invalidate(key));
    console.log(`[Cache] Invalidated ${keysToDelete.length} entries matching '${pattern}'`);
  }

  /**
   * Clear all cache entries
   */
  clear(): void {
    this.cache.clear();
    this.accessOrder = [];
    console.log('[Cache] All entries cleared');
  }

  /**
   * Get cache statistics
   */
  getStats(): { size: number; maxSize: number; hitRate: string } {
    return {
      size: this.cache.size,
      maxSize: this.maxSize,
      hitRate: 'N/A'  // Could track hits/misses for real hit rate
    };
  }

  /**
   * Clear expired cache entries
   */
  private clearExpired(): void {
    const now = Date.now();
    const keysToDelete: string[] = [];

    this.cache.forEach((entry, key) => {
      if (now - entry.timestamp > entry.ttl) {
        keysToDelete.push(key);
      }
    });

    keysToDelete.forEach(key => {
      this.cache.delete(key);
      this.removeFromAccessOrder(key);
    });

    if (keysToDelete.length > 0) {
      console.log(`[Cache] Cleared ${keysToDelete.length} expired entries`);
    }
  }

  /**
   * Evict least recently used entry when cache is full
   */
  private evictLRU(): void {
    if (this.accessOrder.length === 0) return;

    const lruKey = this.accessOrder[0];  // First = least recently used
    this.cache.delete(lruKey);
    this.accessOrder.shift();

    console.log(`[Cache] Evicted LRU entry: ${lruKey}`);
  }

  /**
   * Update access order for LRU tracking
   */
  private updateAccessOrder(key: string): void {
    // Remove from current position
    this.removeFromAccessOrder(key);

    // Add to end (most recently used)
    this.accessOrder.push(key);
  }

  /**
   * Remove key from access order array
   */
  private removeFromAccessOrder(key: string): void {
    const index = this.accessOrder.indexOf(key);
    if (index > -1) {
      this.accessOrder.splice(index, 1);
    }
  }
}
