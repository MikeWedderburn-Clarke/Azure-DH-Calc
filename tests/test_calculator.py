from azure_dh_calc.calculator import requirement_from_vm, plan_options


def test_plan_sorting_by_cost():
    req = requirement_from_vm("D2s_v3", 10)  # 20 vcpu / 80 GiB
    options = plan_options(req)
    # Ensure sorted ascending by monthly cost
    costs = [o.total_monthly_cost for o in options]
    assert costs == sorted(costs)
    # Each option must provide capacity >= requirement
    for o in options:
        assert o.total_vcpus >= req.vcpus
        assert o.total_memory_gib >= req.memory_gib
