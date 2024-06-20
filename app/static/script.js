        // Funzione per aggiornare l'altezza del background-blur
        function updateBackgroundBlurHeight() {
            var pageHeight = document.documentElement.scrollHeight;
            var backgroundBlur = document.getElementById('background-blur');
            backgroundBlur.style.height = pageHeight + 'px';
        }
        
        // Aggiorna l'altezza del background-blur al caricamento della pagina
        window.onload = updateBackgroundBlurHeight;
        
        // Aggiorna l'altezza del background-blur quando la finestra viene ridimensionata
        window.onresize = updateBackgroundBlurHeight;