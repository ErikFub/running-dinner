let map;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
      zoom: 14,
      center: { lat: 38.71022591158496, lng: -9.143924874381959}
  });
  map.setOptions({
      styles: [
          {
              "featureType": "administrative",
              "elementType": "geometry",
              "stylers": [{"visibility": "off"}]
          },
          {
              "featureType": "poi.business",
              "stylers": [{"visibility": "off"}]
          },

          {
              "featureType": "poi.parks",
              "elementType": "labels.icon",
              "stylers": [{"visibility": "off"}]
          },
          {
              "featureType": "road",
              "elementType": "labels.icon",
              "stylers": [{"visibility": "off"}]
          },
          {
              "featureType": "transit",
              "stylers": [{"visibility": "off"}]
          }
          ]}
  )

  map.data.addGeoJson(all_turfs);

  // Utility function to darken or lighten color
  const pSBC=(p,c0,c1,l)=>{
      let r,g,b,P,f,t,h,i=parseInt,m=Math.round,a=typeof(c1)=="string";
      if(typeof(p)!="number"||p<-1||p>1||typeof(c0)!="string"||(c0[0]!='r'&&c0[0]!='#')||(c1&&!a))return null;
      if(!this.pSBCr)this.pSBCr=(d)=>{
          let n=d.length,x={};
          if(n>9){
              [r,g,b,a]=d=d.split(","),n=d.length;
              if(n<3||n>4)return null;
              x.r=i(r[3]=="a"?r.slice(5):r.slice(4)),x.g=i(g),x.b=i(b),x.a=a?parseFloat(a):-1
          }else{
              if(n==8||n==6||n<4)return null;
              if(n<6)d="#"+d[1]+d[1]+d[2]+d[2]+d[3]+d[3]+(n>4?d[4]+d[4]:"");
              d=i(d.slice(1),16);
              if(n==9||n==5)x.r=d>>24&255,x.g=d>>16&255,x.b=d>>8&255,x.a=m((d&255)/0.255)/1000;
              else x.r=d>>16,x.g=d>>8&255,x.b=d&255,x.a=-1
          }return x};
      h=c0.length>9,h=a?c1.length>9?true:c1=="c"?!h:false:h,f=this.pSBCr(c0),P=p<0,t=c1&&c1!="c"?this.pSBCr(c1):P?{r:0,g:0,b:0,a:-1}:{r:255,g:255,b:255,a:-1},p=P?p*-1:p,P=1-p;
      if(!f||!t)return null;
      if(l)r=m(P*f.r+p*t.r),g=m(P*f.g+p*t.g),b=m(P*f.b+p*t.b);
      else r=m((P*f.r**2+p*t.r**2)**0.5),g=m((P*f.g**2+p*t.g**2)**0.5),b=m((P*f.b**2+p*t.b**2)**0.5);
      a=f.a,t=t.a,f=a>=0||t>=0,a=f?a<0?t:t<0?a:a*P+t*p:0;
      if(h)return"rgb"+(f?"a(":"(")+r+","+g+","+b+(f?","+m(a*1000)/1000:"")+")";
      else return"#"+(4294967296+r*16777216+g*65536+b*256+(f?m(a*255):0)).toString(16).slice(1,f?undefined:-2)
  }

  map.data.setStyle(function(feature) {
      const sizeX = 380
      const sizeY = 1100
      const svgMarker = {
          path: "M 182.9 551.7 c 0 0.1 0.2 0.3 0.2 0.3 S 358.3 283 358.3 194.6 c 0 -130.1 -88.8 -186.7 -175.4 -186.9 C 96.3 7.9 7.5 64.5 7.5 194.6 c 0 88.4 175.3 357.4 175.3 357.4 S 182.9 551.7 182.9 551.7 Z M 122.2 187.2 c 0 -33.6 27.2 -60.8 60.8 -60.8 c 33.6 0 60.8 27.2 60.8 60.8 S 216.5 248 182.9 248 C 149.4 248 122.2 220.8 122.2 187.2 Z",
          fillColor: feature.getProperty("marker-color"),
          strokeColor: pSBC(-0.4, feature.getProperty("marker-color")), // darkens marker color by 40%
          fillOpacity: 0.8,
          strokeWeight: 1,
          rotation: 0,
          size: new google.maps.Size(sizeX, sizeY),
          origin: new google.maps.Point(0, 0),
          anchor: new google.maps.Point(sizeX/2, sizeY/2),
          scale: 0.08
      };
      return /** @type {!google.maps.Data.StyleOptions} */({
          strokeColor: feature.getProperty('stroke'),
          strokeWeight: feature.getProperty('stroke-width'),
          strokeOpacity: feature.getProperty('stroke-opactiy'),
          title: "Stage: " + feature.getProperty('name'),
          icon: svgMarker
      });
  });
}