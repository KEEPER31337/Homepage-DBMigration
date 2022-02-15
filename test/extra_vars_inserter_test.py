from extra_vars_inserter.extra_vars_inserter import ExtraVarsInserter

extraVarsInserter = ExtraVarsInserter()
extraVarsInserter.setDBController(oldDB)
extraVarsInserter.insertExtraVars()
