# HttpClient Memory Queue - Optimizaciones Implementadas

## Resumen
Se ha extendido la funcionalidad del `HttpClientInfrastructure` con un sistema de captura de eventos en memoria optimizado que solo se activa cuando es necesario.

## Optimizaciones Clave

### 1. **Activación Condicional**
- La captura de eventos solo se ejecuta si se llama `with_memory_queue()`
- Flag `__memory_enabled` evita verificaciones innecesarias en cada request
- Cero overhead cuando no se usa memory queue

### 2. **Serialización Optimizada**
- Método `_serialize_payload()` con manejo eficiente de tipos
- Usa `json.dumps()` con separadores compactos para reducir tamaño
- Manejo seguro de errores sin excepciones costosas

### 3. **Uso de try_push()**
- Evita bloqueos usando `try_push()` en lugar de `push_async()`
- No bloquea el flujo principal si la cola está llena
- Mejor rendimiento en escenarios de alta concurrencia

### 4. **Gestión de Memoria Eficiente**
- Reutilización de `identity` para request/response del mismo call
- Campos opcionales con valores por defecto para reducir memoria
- Método `reset_memory_state()` para limpiar estado entre operaciones

### 5. **Timestamps Optimizados**
- `RequestDatetime` se captura una sola vez y se reutiliza
- `ResponseDatetime` se genera solo cuando es necesario
- Reduce llamadas a `datetime.utcnow()`

## Uso Recomendado

### Para Captura de Eventos
```python
client = HttpClientInfrastructure()
response = await (client
    .http("https://api.example.com")
    .endpoint("users")
    .with_memory_queue(queue, "User.Create.execute", "user_ops")
    .post(user_data))
```

### Para Máximo Rendimiento (sin captura)
```python
client = HttpClientInfrastructure()
response = await (client
    .http("https://api.example.com")
    .endpoint("health")
    .get())  # Sin with_memory_queue() = sin overhead
```

### Para Reutilización de Cliente
```python
# Operación con memory
await client.with_memory_queue(queue, "Op1").get()

# Reset para nueva operación sin memory
client.reset_memory_state()

# Operación sin memory (más rápida)
await client.endpoint("health").get()
```

## Beneficios de Rendimiento

1. **Cero Overhead**: Sin memory queue, no hay impacto en rendimiento
2. **No Bloqueos**: `try_push()` nunca bloquea el hilo principal
3. **Memoria Eficiente**: Serialización optimizada y limpieza de estado
4. **Reutilización**: Un cliente puede manejar múltiples operaciones
5. **Escalabilidad**: Funciona bien bajo alta concurrencia

## Consideraciones

- La cola tiene capacidad limitada (configurable)
- Si la cola está llena, los eventos se descartan silenciosamente
- Para debugging crítico, considerar usar `push_async()` con timeout
- El `reset_memory_state()` es opcional pero recomendado para reutilización