document.addEventListener('DOMContentLoaded', function(){
  const slider = document.getElementById('budgetSlider');
  const budgetValue = document.getElementById('budgetValue');
  const packageLabel = document.getElementById('budgetPackageLabel');
  const packageName = document.getElementById('packageName');
  const packageDetails = document.getElementById('packageDetails');
  const stageTag = document.getElementById('budgetStageTag');
  const featureOptions = document.getElementById('featureOptions');
  const demoFrame = document.getElementById('demoFrame');
  const paypalContainer = document.getElementById('paypal-button-container');
  const hasBudgetControls = slider && budgetValue && packageLabel && packageName && packageDetails && stageTag && featureOptions && demoFrame;

  let totalAmount = 1200;

  const packageRanges = [
    {min:99, max:999, title:'Стартен пакет', subtitle:'За личен бренд и стартапи', details:'Една страница, контакт форма, основна галерија.', key:'starter', features:['landing','contact','gallery']},
    {min:1000, max:3499, title:'Бизнис пакет', subtitle:'За растечки бизниси', details:'До 5 страници, CMS, многујазичност, презентација.', key:'business', features:['landing','contact','gallery','blog','social','multi']},
    {min:3500, max:5999, title:'Е-трговија пакет', subtitle:'Продавница и автоматизација', details:'Онлајн каталог, кошничка и купони.', key:'commerce', features:['landing','contact','gallery','blog','social','multi','shop','inventory']},
    {min:6000, max:8499, title:'Премиум пакет', subtitle:'Ултра уникатен сајт', details:'3D анимации, AI поддршка и персонален дизајн.', key:'premium', features:['landing','contact','gallery','blog','social','multi','shop','inventory','ai','animations']}
  ];

  const features = [
    {key:'extraPage', label:'Дополнителна страница', description:'+150 €', price:150, default:'starter'},
    {key:'gallery', label:'Галерија', description:'+200 €', price:200, default:'starter'},
    {key:'social', label:'Социјални мрежи', description:'+250 €', price:250, default:'starter'},
    {key:'booking', label:'Систем за закажување', description:'+400 €', price:400, default:'business'},
    {key:'multiLanguage', label:'Повеќејазичност', description:'+500 €', price:500, default:'business'},
    {key:'seo', label:'SEO оптимизација', description:'+600 €', price:600, default:'business'},
    {key:'blog', label:'Блог', description:'+700 €', price:700, default:'business'},
    {key:'invoices', label:'PDF фактури', description:'+600 €', price:600, default:'commerce'},
    {key:'coupons', label:'Купони', description:'+800 €', price:800, default:'commerce'},
    {key:'inventory', label:'ERP/магацин', description:'+900 €', price:900, default:'commerce'},
    {key:'aiBot', label:'AI чет-бот', description:'+1.000 €', price:1000, default:'premium'},
    {key:'premiumCare', label:'Премиум поддршка', description:'+1.499 €', price:1499, default:'premium'}
  ];

  function clamp(value, min, max){ return Math.min(Math.max(value, min), max); }

  function findPackage(amount){
    return packageRanges.find(pkg => amount >= pkg.min && amount <= pkg.max) || packageRanges[packageRanges.length-1];
  }

  function formatAmount(amount){
    return amount.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ') + ' €';
  }

  function buildFeatureControls(base){
    featureOptions.innerHTML = '';
    features.forEach(feature => {
      const isChecked = base.key === feature.default || packageRanges.indexOf(base) > packageRanges.findIndex(p => p.key === feature.default);
      const wrapper = document.createElement('label');
      wrapper.className = 'feature-toggle';
      wrapper.innerHTML = `
        <input type="checkbox" data-feature="${feature.key}" data-price="${feature.price}" ${isChecked ? 'checked' : ''}>
        <div>
          <strong>${feature.label}</strong>
          <p>${feature.description}</p>
        </div>
      `;
      const input = wrapper.querySelector('input');
      input.addEventListener('change', updateFromControls);
      featureOptions.appendChild(wrapper);
    });
  }

  function getSelectedFeatures(){
    return Array.from(featureOptions.querySelectorAll('input[type="checkbox"]'))
      .filter(input => input.checked)
      .map(input => {
        const feature = features.find(item => item.key === input.dataset.feature);
        return feature ? feature : { label: input.dataset.feature, price: Number(input.dataset.price) };
      });
  }

  function renderPreview(pkg, selected){
    const selectedItems = selected.map(feature => `<div class="item"><strong>${feature.label}</strong><span>${feature.description}</span></div>`).join('');
    const content = `<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
      body{margin:0;font-family:Inter,system-ui,sans-serif;background:#eef5ff;color:#10263c}
      .frame{padding:24px;}
      .frame-title{margin:0 0 10px;font-size:1.35rem;font-weight:800;}
      .frame-subtitle{margin:0 0 22px;color:#475569;line-height:1.6;}
      .frame-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:14px;}
      .item{padding:16px;border-radius:18px;background:#fff;border:1px solid rgba(16,24,40,.08);box-shadow:0 14px 35px rgba(16,24,40,.06);}
      .item strong{display:block;margin-bottom:8px;font-size:1rem;color:#10263c;}
      .item span{font-size:.92rem;color:#64748b;line-height:1.5;}
      .badge{display:inline-flex;padding:10px 14px;border-radius:999px;background:rgba(47,128,237,.14);color:#1b4edc;font-weight:700;margin-top:14px;}
    </style></head><body>
      <div class="frame">
        <h1 class="frame-title">${pkg.title}</h1>
        <div class="frame-subtitle">${pkg.details}</div>
        <div class="badge">${formatAmount(totalAmount)}</div>
        <div class="frame-grid">
          <div class="item"><strong>Пакет</strong><span>${pkg.subtitle}</span></div>
          ${selectedItems}
        </div>
      </div>
    </body></html>`;
    demoFrame.srcdoc = content;
  }

  function updateFromControls(){
    const amount = Number(slider.value);
    const pkg = findPackage(amount);
    const selected = getSelectedFeatures();
    let computed = pkg.min;
    selected.forEach(feature => { computed += feature.price; });
    totalAmount = clamp(computed, 99, 8499);
    slider.value = totalAmount;
    budgetValue.textContent = formatAmount(totalAmount);
    packageLabel.textContent = pkg.title;
    packageName.textContent = pkg.subtitle;
    packageDetails.textContent = pkg.details;
    stageTag.textContent = pkg.title;
    renderPreview(pkg, selected);
    renderPayPalButton();
  }

  function initialize(){
    const basePkg = findPackage(Number(slider.value));
    buildFeatureControls(basePkg);
    budgetValue.textContent = formatAmount(Number(slider.value));
    packageLabel.textContent = basePkg.title;
    packageName.textContent = basePkg.subtitle;
    packageDetails.textContent = basePkg.details;
    stageTag.textContent = basePkg.title;
    renderPreview(basePkg, getSelectedFeatures());
    renderPayPalButton();
  }

  function renderPayPalButton(){
    if(!window.paypal || !paypalContainer) return;
    paypalContainer.innerHTML = '';
    paypal.Buttons({
      style: { layout:'vertical', color:'blue', shape:'pill', label:'pay' },
      createOrder(data, actions){
        return actions.order.create({
          purchase_units:[{ amount:{ value: totalAmount.toString() } }]
        });
      },
      onApprove(data, actions){
        return actions.order.capture().then(details => {
          alert('Плаќањето е успешно! Вкупно: ' + totalAmount + ' €');
        });
      }
    }).render(paypalContainer);
  }

  function initBackground(){
    const canvas = document.getElementById('backgroundScene');
    if(!canvas) return;
    const ctx = canvas.getContext('2d');
    let width = 0;
    let height = 0;
    const nodes = Array.from({length:70}, () => ({
      x: 0, y: 0, vx:(Math.random()-0.5)*0.4, vy:(Math.random()-0.5)*0.4, size: Math.random()*1.5 + 0.8
    }));
    const mouse = {x: window.innerWidth/2, y: window.innerHeight/2};

    function resize(){
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
      nodes.forEach(node => { node.x = Math.random()*width; node.y = Math.random()*height; });
    }

    function draw(){
      ctx.clearRect(0,0,width,height);
      nodes.forEach(node => {
        node.x += node.vx;
        node.y += node.vy;
        if(node.x < -20) node.x = width + 20;
        if(node.x > width + 20) node.x = -20;
        if(node.y < -20) node.y = height + 20;
        if(node.y > height + 20) node.y = -20;
        const dx = node.x - mouse.x;
        const dy = node.y - mouse.y;
        const dist = Math.hypot(dx, dy);
        if(dist < 140){ node.vx += dx * 0.0008; node.vy += dy * 0.0008; }
        ctx.beginPath();
        ctx.arc(node.x, node.y, node.size, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(47,128,237,0.18)';
        ctx.fill();
      });
      nodes.forEach((a,i) => {
        for(let j=i+1;j<nodes.length;j++){
          const b = nodes[j];
          const d = Math.hypot(a.x-b.x, a.y-b.y);
          if(d < 120){
            ctx.strokeStyle = `rgba(47,128,237,${1 - d/120})`;
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(a.x,a.y);
            ctx.lineTo(b.x,b.y);
            ctx.stroke();
          }
        }
      });
      requestAnimationFrame(draw);
    }

    window.addEventListener('resize', resize);
    window.addEventListener('mousemove', e => { mouse.x = e.clientX; mouse.y = e.clientY; });
    resize();
    draw();
  }

  if (slider) {
    slider.addEventListener('input', updateFromControls);
  }

  if (hasBudgetControls) {
    initialize();
  }

  initBackground();
});