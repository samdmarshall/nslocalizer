//
//  DetailViewController.h
//  pylocalizer-example
//
//  Created by Samantha Marshall on 7/27/16.
//  Copyright © 2016 Samantha Marshall. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface DetailViewController : UIViewController

@property (strong, nonatomic) id detailItem;
@property (weak, nonatomic) IBOutlet UILabel *detailDescriptionLabel;

@end

