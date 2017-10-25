def jaeger(name):
    from jaeger_client import Config
    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'local_agent': {
                'reporting_host': '127.0.0.1',
                'reporting_port': 5775,
            },
        },
        service_name=name,
    )
    return config.initialize_tracer()


def lightstep(name):
    import lightstep.tracer
    ls_tracer = lightstep.tracer.init_tracer(group_name=name, access_token="{your_lightstep_token}")
    return ls_tracer
