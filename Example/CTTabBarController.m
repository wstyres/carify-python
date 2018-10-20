#import "CTTabBarController.h"
#import "CTRootViewController.h"

@implementation CTTabBarController

- (void)loadView {
  [super loadView];

  UINavigationController *firstController = [[UINavigationController alloc] initWithRootViewController:[[CTRootViewController alloc] init]];
  UITabBarItem *firstIcon = [[UITabBarItem alloc] initWithTitle:@"First" image:[UIImage imageNamed:@"First.png"] selectedImage:[UIImage imageNamed:@"First.png"]];
  [firstController setTabBarItem:firstIcon];

  UINavigationController *secondController = [[UINavigationController alloc] initWithRootViewController:[[CTRootViewController alloc] init]];
  UITabBarItem *secondIcon = [[UITabBarItem alloc] initWithTitle:@"Second" image:[UIImage imageNamed:@"Second.png"] selectedImage:[UIImage imageNamed:@"Second.png"]];
  [secondController setTabBarItem:secondIcon];

  self.viewControllers = [NSArray arrayWithObjects:firstController, secondController, nil];
}

@end
