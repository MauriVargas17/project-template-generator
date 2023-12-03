# Segundo Proyecto

## Mauricio Vargas Escobar

## 56224

### Descripcion

Este proyecto contiene una API desplegada en un contenedor de Docker
a traves del servicio GCP en la direccion:

```
https://project-template-generator-ejagmyulda-uc.a.run.app/docs
```

La API se basa en analisis de contenido fundamentalmente en ingles.

Contiene 5 endpoints:

- /status: Retorna el estado, version y modelos alojados
- /sentiment: Retorna un analisis de sentimiento de un texto financiero, confidence, valor en un rango de -1 a 1 y una etiqueta
  descriptiva desde muy negativo a muy positivo. Se usa el modelo ProsusAI/finbert
- /analysis: Retorna un analisis mas completo del texto financiero,
  donde se provee el POS, NER, Embedding, Sentiment y demas. Se usa el modelo en_core_web_sm
- /analysis_v2: Retorna el mismo analisis que el anterior endpoint pero utilizando el modelo GPT-4 para generar mejores respuestas.
- /reports: Retorna en formato CSV todas las entradas realizadas durante la sesion activa a traves del endpoint /analysis.
