from risk_engine import RiskAssessment, risk_matrix_score, sort_risks


def test_risk_score_and_priority():
    risk = RiskAssessment("Gevel", 5, 80, 70, 60, 50)
    assert risk.condition_risk == 80.0
    assert risk.risk_score == 74.0
    assert risk.priority == "HOOG"


def test_risk_matrix():
    assert risk_matrix_score(80, 50) == 40.0


def test_sort_risks():
    low = RiskAssessment("Dak", 2, 20, 20)
    high = RiskAssessment("Lift", 6, 90, 90)
    assert [item.component for item in sort_risks([low, high])] == ["Lift", "Dak"]
