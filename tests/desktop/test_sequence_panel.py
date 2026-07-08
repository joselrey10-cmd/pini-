from pini_desktop.services.editor.optimization.chain_evaluator import SequenceScore
from pini_desktop.services.editor.optimization.move_sequence import MoveSequence, MoveStep
from pini_desktop.services.editor.optimization.sequence_apply_service import SequenceApplyService

def test_sequence_apply_service_can_be_created():
    assert SequenceApplyService() is not None

def test_sequence_preview_dialog_import():
    from pini_desktop.ui.views.sequence_preview_dialog import SequencePreviewDialog
    assert SequencePreviewDialog is not None

def test_sequence_optimizer_panel_import():
    from pini_desktop.ui.views.sequence_optimizer_panel import SequenceOptimizerPanel
    assert SequenceOptimizerPanel is not None

def test_sequence_score_shape():
    seq = MoveSequence(steps=(MoveStep(1, 1, 2, 3, 1.2, "Mover"),))
    score = SequenceScore(sequence=seq, score=1.2, risk=0.1, recommendation="OK")
    assert score.sequence.length == 1
    assert score.score == 1.2
