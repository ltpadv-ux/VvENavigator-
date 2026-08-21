from src.ga_release_execution_immutable_evidence_archive import finalize_ga_release

def _ready(): return {'ga_tag_ready':True,'decision':'TAG-READY'}
def _exec(): return {'tag':'v18.2.0','commit_sha':'abc','tag_created':True,'release_created':True,'production_published':True}
def _archive(): return {'archive_ref':'archive://ga/v18.2.0','checksum_sha256':'deadbeef','immutable':True}
def test_complete_ga_release_closes():
 x=finalize_ga_release(_ready(),_exec(),_archive()); assert x['ga_release_completed'] is True and x['status']=='GA RELEASE COMPLETED'
def test_missing_archive_blocks_completion():
 x=finalize_ga_release(_ready(),_exec(),{}); assert x['ga_release_completed'] is False and 'IMMUTABLE_EVIDENCE_ARCHIVE_INCOMPLETE' in x['blockers']
def test_no_automatic_release_or_tagging():
 x=finalize_ga_release({}, {}, {}); assert x['automatic_release'] is False and x['automatic_tagging'] is False
