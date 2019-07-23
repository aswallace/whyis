from .unit_test_case import UnitTestCase


class AgentUnitTestCase(UnitTestCase):
    def run_agent(self, agent, nanopublication=None):
        app = self.app
        agent.dry_run = True
        agent.app = app
        results = []
        if nanopublication is not None:
            results.extend(agent.process_graph(nanopublication))
        elif agent.query_predicate == app.NS.whyis.globalChangeQuery:
            results.extend(agent.process_graph(app.db))
        else:
            print("Running as update agent")
            for resource in agent.getInstances(app.db):
                print(resource.identifier)
                for np_uri, in app.db.query('''select ?np where {
        graph ?assertion { ?e ?p ?o.}
        ?np a np:Nanopublication;
            np:hasAssertion ?assertion.
    }''', initBindings={'e': resource.identifier}, initNs=app.NS.prefixes):
                    print(np_uri)
                    np = app.nanopub_manager.get(np_uri)
                    results.extend(agent.process_graph(np))
        return results