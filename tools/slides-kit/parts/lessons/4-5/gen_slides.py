# Generates slides.html for Lesson 4.5. Placeholder (workshop step 02): a cover only, so that build.py 4 5 --out works.
# Step 04 replaces this file with the 27 slides of plan section 5.
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'slides.html')
html = '''<main id="stage">
<div id="prog"><i></i></div>
<section class="slide t-cover" id="s01" data-period="1" data-title="Bonds, forces and properties" data-sec="Lesson 4.5" data-ref="Reading §4.5">
  <h2>Bonds, forces and properties</h2>
  <div class="body">
    <div class="card dq reg"><p class="tag">Driving question</p><p>How do the forces within and between particles explain the melting point, conductivity and hardness of a substance?</p></div>
  </div>
  <aside class="notes">Placeholder cover written in workshop step 02. Step 04 builds the deck.</aside>
  <script>Deck.frames('s01',[
    {t:0.5,note:"Placeholder cover (workshop step 02)."}
  ]);</script>
</section>

<footer id="foot"><span id="sec"></span><span id="cue"></span><span id="count"></span></footer>
</main>
<div id="notes" hidden></div>
<div id="overview" hidden></div>
<div id="blank" hidden></div>
<div id="runsheet"></div>
<script>Deck.start()</script>
</body>
</html>
'''
open(OUT, 'w', encoding='utf-8', newline='').write(html)
print('slides: 1 (placeholder cover)')
