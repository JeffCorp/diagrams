'''
Created on 2020-02-13

@author: wf
'''
import unittest
from dgs.diagrams import Command,Generator,Generators,Example
debug=True
class TestDiagrams(unittest.TestCase):
    """ Test the diagrams service"""
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCommands(self):
        cmds=[Command("pwd","",debug=True),Command("java","-version",debug=True),Command("dot","-V",debug=True),Command("mscgen","",debug=True)]
        for cmd in cmds:
            cmd.check()
        pass
    
    def testGetGenerator(self):
        generators=["graphviz","mscgen","plantuml"]
        for generator in generators:
            gen=Generators.get(generator)
            assert gen is not None
            info=gen.getHtmlInfo()
            if debug:
                print(info)
    
    def testGeneratorCheck(self):
        for gen in Generators.generators():
            gen.debug=debug
            gen.check()
            
    def testGeneratorVersion(self):
        for gen in Generators.generators():
            gen.debug=debug
            version=gen.getVersion()    
            if debug:
                print(version)    
                
    def testGeneratorForAlias(self):
        for gen in Generators.generators():
            gen.debug=debug
            for alias in gen.aliases:
                genid=Generators.generatorIdForAlias(alias)
                assert genid==gen.id
            
    def testExamples(self):
        for gen in Generators.generators():
            for alias in gen.aliases:
                txt=Example.get(alias)
                if debug:
                    print (txt)
                assert not "no example for" in txt            

    def testGenerators(self):
        if debug:
            print ("outputDirectory is: %s" % (Generator.getOutputDirectory()))
        for gen in Generators.generators():
            gen.debug=debug
            for alias in gen.aliases:
                txt=Example.get(alias)
                result=gen.generate(alias,txt,gen.defaultType)
                valid =result.isValid()
                if not valid:
                    print(result.errMsg())
                assert valid
            
    def testGenerateResult(self):
        genid=Generators.generatorIdForAlias("plantuml")
        gen=Generators.get(genid)
        # provoke an error
        result=gen.generate('unknownalias','garbage input',gen.defaultType)    
        json=result.asJson('http://www.doe.com') 
        assert "error" in json
                    
    def testDecodeImage(self):
        pass            

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testDiagrams']
    unittest.main()