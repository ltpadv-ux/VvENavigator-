from src.backup_restore_data_integrity_disaster_recovery import verify_disaster_recovery

def test_full_dr_evidence_passes():
 b={'backup_id':'B1','completed':True,'encrypted':True,'offsite_copy':True}; r={'restore_id':'R1','completed':True,'rto_minutes':120,'rpo_minutes':60}; i={'checksum_match':True,'rowcount_match':True,'schema_match':True,'referential_integrity_ok':True}; x=verify_disaster_recovery(b,r,i); assert x['production_recovery_ready'] is True

def test_checksum_mismatch_blocks():
 b={'completed':True,'encrypted':True,'offsite_copy':True}; r={'completed':True,'rto_minutes':120,'rpo_minutes':60}; i={'checksum_match':False,'rowcount_match':True,'schema_match':True,'referential_integrity_ok':True}; x=verify_disaster_recovery(b,r,i); assert 'CHECKSUM_MISMATCH' in x['blockers']

def test_no_automatic_restore_or_failover():
 x=verify_disaster_recovery({}, {}, {}); assert x['automatic_restore'] is False and x['automatic_failover'] is False
