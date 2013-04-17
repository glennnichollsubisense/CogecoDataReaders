import XLSToSWExceptions
import operator


class XLSToSWCustomEnumeratorGenerator():

    s_slot=0
    s_valid_cogeco_enumerator_names=['cogeco_class', 'cogeco_node_type', 'cogeco_route_crossing', 'cogeco_sheath_usage', 'cogeco_size', 'cogeco_fixture_size', 'cogeco_ground_type', 'cogeco_guy_size', 'cogeco_installation_method', 'cogeco_operational_status', 'cogeco_owner', 'cogeco_usage', 'cogeco_nap_type', 'cogeco_port_connection_type', 'cogeco_representation', 'cogeco_status', 'cogeco_strands', 'cogeco_users', 'cogeco_waterway_type', 'cogeco_transportation_route_type']
    s_valid_sovernet_enumerator_names=['sov_guy_type','sov_placement','sov_pole_attachment','sov_att_fcc','sov_el_tel','sov_attachment_type','sov_pole_source','sov_pole_owner','sov_ug_owner','sov_leased_fiber_owner']


    def __init__(self):

        self.s_slot=1       



    def customEnums(self, pCustomerName='Cogeco'):

        if pCustomerName=='Cogeco':
            return self.s_valid_cogeco_enumerator_names

        if pCustomerName=='Sovernet':
            return self.s_valid_sovernet_enumerator_names


if __name__ == "__main__":
    l_me = XLSToSWCustomEnumeratorGenerator()
    
    


