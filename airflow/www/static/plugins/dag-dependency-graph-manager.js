class GraphManager {

    constructor(graphObject) {
        this.computeNodeSet = new Set([]);
        this.graphObject = graphObject;
    }

    getGraph(dag_id, degree, downstream) {
        let e = this.computeEdges(this.graphObject.edges, dag_id, degree, downstream);
        return {
            nodes : this.getNodes(e, this.graphObject.nodes, dag_id),
            edges : this.getEdges(e)
        }
    }
    
    formatNode(node) {
        return {
            'id': node,
            'value': {
                'label': node
            }
        }
    }

    formatEdge(edge) {
        return {
            'id'    : edge[0]+edge[1],
            'u'     : edge[0],
            'v'     : edge[1],
            'value' : edge[0]+edge[1]
        }
    }

    getNodes(edges, nodes, dag_id) {
        let n = [];
        let nodeSet = new Set(['']);

        for (let i = 0 ; i < edges.length ; i++) {
            if (!nodeSet.has(edges[i][0])) {
                n.push(this.formatNode(edges[i][0]));
                nodeSet.add(edges[i][0]);
            }
            if (!nodeSet.has(edges[i][1])) {
                n.push(this.formatNode(edges[i][1]));
                nodeSet.add(edges[i][1])
            }
        }

        if (dag_id == '') {
            for (let i = 0 ; i < nodes.length ; i++) {
                if (!nodeSet.has(nodes[i])) {
                    n.push(this.formatNode(nodes[i]));
                    nodeSet.add(nodes[i]);
                }
            }
        }

        if (dag_id != '' && !nodeSet.has(dag_id)) {
            n.push(this.formatNode(dag_id));
            nodeSet.add(dag_id);
        }
        return n;
    }

    getEdges(e) {
        let edges = [];
        for (let i = 0 ; i < e.length ; i++) {
            edges.push(this.formatEdge(e[i]));
        }
        return edges;
    }

    computeEdges(graph, dag_id, degree, downstream) {
        this.computeNodeSet.clear();
        return this.computeEdgesHelper(graph, dag_id, degree, downstream);
    }

    computeEdgesHelper(graph, dag_id, degree, downstream) {
        if (degree == 0) {
            return [];
        }

        let edges = [];
        if (dag_id == '') {
            for (let i = 0 ; i < graph.length ; i++) {
                edges.push([graph[i][0], graph[i][1]]);
            }
            return edges;
        }

        for (let i = 0 ; i < graph.length ; i++) {
            let pivot = 0;
            if (!downstream) {
                pivot = 1;
            }
            if (graph[i][pivot] == dag_id) {
                edges.push([graph[i][0], graph[i][1]]); 
                this.computeNodeSet.add(graph[i][pivot]);
                if (!this.computeNodeSet.has(graph[i][Math.abs(pivot-1)])) {
                    let downstreamEdges = this.computeEdgesHelper(graph, graph[i][Math.abs(pivot-1)], degree - 1, downstream);
                    for (let j = 0 ; j < downstreamEdges.length ; j++) {
                        edges.push(downstreamEdges[j]);
                    }
                }
            }
        }
        return edges;
    }
}
