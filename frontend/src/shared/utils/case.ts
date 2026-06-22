export function snakeToCamel(str: string): string {
  return str.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase())
}

export function camelToSnake(str: string): string {
  return str.replace(/[A-Z]/g, (letter) => `_${letter.toLowerCase()}`)
}

export function transformKeys<T>(obj: unknown, fn: (str: string) => string): T {
  if (obj === null || obj === undefined) return obj as T
  if (Array.isArray(obj)) return obj.map((item) => transformKeys(item, fn)) as T
  if (typeof obj === "object" && obj.constructor === Object) {
    const result: Record<string, unknown> = {}
    for (const [key, value] of Object.entries(obj)) {
      result[fn(key)] = transformKeys(value, fn)
    }
    return result as T
  }
  return obj as T
}

export function snakeToCamelObj<T>(obj: unknown): T {
  return transformKeys<T>(obj, snakeToCamel)
}

export function camelToSnakeObj<T>(obj: unknown): T {
  return transformKeys<T>(obj, camelToSnake)
}
