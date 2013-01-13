'use strict';

/* http://docs.angularjs.org/guide/dev_guide.e2e-testing */

describe('my app', function() {

  beforeEach(function() {
    browser().navigateTo('../../app/index.html');
  });


  it('should automatically redirect to /view1 when location hash/fragment is empty', function() {
    expect(browser().location().url()).toBe("/lobby");
  });


  describe('lobby', function() {

    beforeEach(function() {
      browser().navigateTo('#/lobby');
    });


    it('should render list of games', function() {
      expect(element('[ng-view] #games').text()).
        toMatch(/.*/);
    });

  });


  describe('tictactoe', function() {

      beforeEach(function() {
	  browser().navigateTo('#/tictactoe');
      });


      it('should render the tictactoe board when user navigates to #/tictactoe',
	 function() {
	     expect(element('table tr').count()).
		 toEqual(3);
	 });

  });
});
