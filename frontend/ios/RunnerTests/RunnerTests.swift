import XCTest
@testable import Runner

class RunnerTests: XCTestCase {

    var appDelegate: AppDelegate!
    var window: UIWindow!

    override func setUp() {
        super.setUp()
        
        // Use these lines to set up your UI tests
        appDelegate = UIApplication.shared.delegate as? AppDelegate
        window = UIWindow(frame: UIScreen.main.bounds)
        window.makeKeyAndVisible()
        let storyboard = UIStoryboard(name: "Main", bundle: nil)
        let navigationController = storyboard.instantiateViewController(withIdentifier: "NavigationController")
        appDelegate?.window??.rootViewController = navigationController
    }

    func testExample() {
        // If you add code to the Runner application, consider adding tests here.
        // Use this method to test basic UI functionality of your app
        let firstViewController = appDelegate.window??.rootViewController as? FirstViewController
        XCTAssertNotNil(firstViewController)
        
        firstViewController?.someMethod()
        XCTAssertTrue(firstViewController?.someProperty ?? false)
    }

}
