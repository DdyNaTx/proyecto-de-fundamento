<?php

class Router {
    public $name;
    public $links = [];

    public function __construct($name) {
        $this->name = $name;
    }

    public function addLink($router) {
        $this->links[] = $router;
    }

    public function removeLink($router) { 
        $index = array_search($router, $this->links);
        unset($this->links[$index]);
    }

    public function printRoutes() {
        echo $this->name . ": "; 
        foreach ($this->links as $link) {
            echo $link->name ." "; 
        } 
        echo "\n";
    }
}

function createTopology($routers) {
    $r1 = $routers[0]; $r2 = $routers[1]; $r3 = $routers[2];

    $r1->addLink($r2); $r1->addLink($r3);
    $r2->addLink($r1); $r2->addLink($r3);
    $r3->addLink($r1); $r3->addLink($r2);
}

function breakLink($r1, $r2) {
    $r1->removeLink($r2);  
    $r2->removeLink($r1);
}

function simulate($routers) {    
    echo "Inicializando simulación...\n";
    printRoutes($routers);
    
    $r1 = $routers[array_rand($routers)];  
    $r2 = $routers[array_rand($routers)];
    
    echo "Desconectando enlace entre $r1->name y $r2->name\n";
    
    breakLink($r1, $r2);  
    
    echo "Nueva topología: \n";
    printRoutes($routers);  
    
    echo "Recalculando rutas...\n";
    foreach($routers as $r) {
        echo $r->name . ": recalculando rutas\n";
    }   
    echo "Convergencia completada\n";
}

function printRoutes($routers) {
    foreach($routers as $r) {
        $r->printRoutes();
    }
}  

$routers = [
    new Router("R1"),  
    new Router("R2"),
    new Router("R3")
];

createTopology($routers);
simulate($routers);

?>