
// Some of this code is originally from STL loader test by aleeper https://github.com/aleeper
if ( ! Detector.webgl ) Detector.addGetWebGLMessage();

var container;

var camera, cameraTarget, scene, renderer;

init();
animate();

var width = window.innerWidth;
var height = window.innerHeight;

function init() {

    // must assign window. inner__ to variables or else can't later divide size
    var width = window.innerWidth;
    var height = window.innerHeight;

    container = document.createElement( 'div' );
    document.body.appendChild( container );

    camera = new THREE.PerspectiveCamera( 30, width / height, 1, 15 );
    camera.position.set( 3, 0.15, 3 );

    cameraTarget = new THREE.Vector3( 0, -0.25, 0 );

    scene = new THREE.Scene();
    scene.fog = new THREE.Fog( 0xb3ddf9, 1, 15 );


    // Ground

    var plane = new THREE.Mesh(
        new THREE.PlaneBufferGeometry( 40, 40 ),
        new THREE.MeshPhongMaterial( { color: 0xdef0fc, specular: 0x101010 } )
    );
    plane.rotation.x = -Math.PI/2;
    plane.position.y = -0.5;
    scene.add( plane );

    plane.receiveShadow = true;


    var loader = new THREE.STLLoader();


    // Load STL file
    var material = new THREE.MeshPhongMaterial( { color: 0x7a8699, specular: 0x111111, shininess: 200 } );

    loader.load( '/uploaded/stl_files/projectminiverese_text.stl', function ( geometry ) {

        var mesh = new THREE.Mesh( geometry, material );

        mesh.position.set( 0, - 0.37, - 0.6 );
        mesh.rotation.set( - Math.PI / 2, 0, 0 );
        mesh.scale.set( 1, 1, 1 );

        mesh.castShadow = false;
        mesh.receiveShadow = true;

        scene.add( mesh );

    } );


    // Lights
    scene.add( new THREE.HemisphereLight( 0x443333, 0x111122 ) );

    addShadowedLight( 1, 1, 1, 0xffffff, 1 );
    addShadowedLight( 0.5, 1, -1, 0xe0e9f9, 0.6 );

    // renderer

    renderer = new THREE.WebGLRenderer( { antialias: true } );
    renderer.setClearColor( scene.fog.color );
    renderer.setPixelRatio( window.devicePixelRatio );
    renderer.setSize( width/2, height/2 );

    renderer.gammaInput = true;
    renderer.gammaOutput = true;

    renderer.shadowMap.enabled = true;
    renderer.shadowMap.renderReverseSided = false;

    container.appendChild( renderer.domElement );


    window.addEventListener( 'resize', onWindowResize, false );

    // Adds orbit controls
    controls = new THREE.OrbitControls(camera, renderer.domElement);
}

function addShadowedLight( x, y, z, color, intensity ) {

    var directionalLight = new THREE.DirectionalLight( color, intensity );
    directionalLight.position.set( x, y, z );
    scene.add( directionalLight );

    directionalLight.castShadow = true;

    var d = 1;
    directionalLight.shadow.camera.left = -d;
    directionalLight.shadow.camera.right = d;
    directionalLight.shadow.camera.top = d;
    directionalLight.shadow.camera.bottom = -d;

    directionalLight.shadow.camera.near = 1;
    directionalLight.shadow.camera.far = 4;

    directionalLight.shadow.mapSize.width = 1024;
    directionalLight.shadow.mapSize.height = 1024;

    directionalLight.shadow.bias = -0.005;

}

function onWindowResize() {

    camera.aspect = width / height;
    camera.updateProjectionMatrix();

    renderer.setSize( width/2, height/2 );

}

function animate() {

    requestAnimationFrame( animate );

    render();
    // stats.update();

}

function render() {
    // Makes the model(s) spin slower or faster, optional
        var timer = Date.now() * 0.0005;
        // Distance from objects
        camera.position.x = Math.cos( timer ) * 2;
        camera.position.z = Math.sin( timer ) * 2;

    camera.lookAt( cameraTarget );

    renderer.render( scene, camera );

    controls.update();
}
