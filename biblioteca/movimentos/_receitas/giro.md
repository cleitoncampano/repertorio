## Receita com o motor

2D: mesmo `data-m` com `rotate` diferente no slide B.

3D (modelo .glb):

```html
<script type="module" src="https://cdn.jsdelivr.net/npm/@google/model-viewer@3.5.0/dist/model-viewer.min.js"></script>
<model-viewer src="objeto.glb" camera-orbit="0deg 75deg 2.5m" interpolation-decay="120" disable-zoom
  style="position:absolute;right:0;top:0;width:1100px;height:1080px"></model-viewer>
<script>
  // a cada slide, gire a câmera: document.querySelector('model-viewer').cameraOrbit = '120deg 70deg 1.6m'
</script>
```

- Os modelos 3D do acervo saem com `python3 -I ferramentas/midia.py <id> pasta` (busque com `--doc midia --uso 3d`).
- Sem 3D: PNGs recortados do objeto em ângulos diferentes, mesmo `data-m`.
