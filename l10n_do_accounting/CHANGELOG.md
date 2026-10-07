# Cambios

## 19.0.0.6
- **QR / timbre del e-CF:** una sola implementación (`_l10n_do_build_stamp_url`) que `l10n_do_ecf`
  reutiliza. Reproduce exactamente el formato de producción (verificado con los 33 e-CF de JCG:
  33/33 idénticos), y corrige los fallos de la versión de este módulo: un valor vacío salía como
  "False" en la URL y se codificaba la URL completa (`https%3A%2F%2F...`).
- **Contingencia:** `l10n_do_company_in_contingency` ya no mira los e-CF de TODAS las compañías
  (en multi-compañía una compañía heredaba el estado de otra) ni escribe dentro del compute.
- **RNC obligatorio del comprador:** validación al confirmar facturas de venta fiscales (antes estaba
  comentada). Exige RNC/Cédula en los comprobantes con "RNC requerido" y en consumo desde el umbral
  (B02 sin ITBIS, e-CF 32 con total). Se valida ANTES de confirmar para no consumir secuencia ni
  generar el e-CF. Solo afecta facturas que se confirmen de ahora en adelante.
- **Ajustes (con ayuda):** "Require buyer RNC/Cédula" y "Consumer invoice threshold (RD$)".
