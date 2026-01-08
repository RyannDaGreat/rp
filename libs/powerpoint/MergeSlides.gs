/**
 * THIS SCRIPT IS NOT USED IN THE PYTHON CODEBASE. THIS IS FOR REFERENCE. IT LIVES ONLINE, AT 
 * https://script.google.com/home/projects/1zWUiYdF8iBHmDu4vsOpDS6JR8nXOiXr1qCec5FmbhAZqUrZsdr8tMv1s/edit
 * Google Apps Script Web App for merging slides.
 *
 * DEPLOYMENT INSTRUCTIONS:
 * 1. Go to https://script.google.com/home
 * 2. Create a new project, paste this code
 * 3. Deploy > New deployment > Web app
 * 4. Execute as: "Me"
 * 5. Who has access: "Anyone" (NOT "Anyone with Google account" - must be "Anyone")
 * 6. Click Deploy, authorize when prompted
 * 7. Copy the deployment URL
 * 8. Update MERGE_WEBAPP_URL in google_slides_upload.py
 *
 * TO UPDATE EXISTING DEPLOYMENT:
 * 1. Deploy > Manage deployments
 * 2. Click the pencil icon to edit
 * 3. Change "Who has access" to "Anyone"
 * 4. Click Deploy
 */

// Simple GET handler to verify deployment works
function doGet(e) {
  return ContentService.createTextOutput(JSON.stringify({
    status: 'ok',
    message: 'MergeSlides web app is running'
  })).setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    var presentationIds = data.presentationIds;
    var mergedName = data.mergedName || 'Merged Presentation';

    // Create a new presentation
    var merged = SlidesApp.create(mergedName);

    // Remove the default blank slide
    var defaultSlides = merged.getSlides();
    if (defaultSlides.length > 0) {
      defaultSlides[0].remove();
    }

    // Copy slides from each source presentation in order
    for (var i = 0; i < presentationIds.length; i++) {
      var source = SlidesApp.openById(presentationIds[i]);
      var sourceSlides = source.getSlides();

      for (var j = 0; j < sourceSlides.length; j++) {
        merged.appendSlide(sourceSlides[j]);
      }
    }

    return ContentService.createTextOutput(JSON.stringify({
      success: true,
      presentationId: merged.getId(),
      url: merged.getUrl(),
      slideCount: merged.getSlides().length
    })).setMimeType(ContentService.MimeType.JSON);

  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({
      success: false,
      error: error.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

// For testing in the Apps Script editor
function testMerge() {
  var result = doPost({
    postData: {
      contents: JSON.stringify({
        presentationIds: ['PASTE_ID_1_HERE', 'PASTE_ID_2_HERE'],
        mergedName: 'Test Merge'
      })
    }
  });
  Logger.log(result.getContent());
}
